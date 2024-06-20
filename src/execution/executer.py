import os
import json
import logging
import re
import json

from pm4py.objects.bpmn.obj import BPMN
from src.repository.repository import Repository
from src.execution.handler import FunctionSelector, ParameterAssignator
from src.execution.prompt_exclusive_gateway import get_sys_message, get_prompt
from src.modelling.workflow_processor import WorkflowProcessor
from src.utils.open_ai import OpenAIConnection


# Define type hints
from typing import Tuple, TypeAlias
StartEvent: TypeAlias = BPMN.StartEvent
EndEvent: TypeAlias = BPMN.EndEvent
Task: TypeAlias = BPMN.Task
ExclusiveGateway: TypeAlias = BPMN.ExclusiveGateway
ParallelGateway: TypeAlias = BPMN.ParallelGateway
Node: TypeAlias = BPMN.BPMNNode
Edge: TypeAlias = BPMN.Flow
    
class WorkflowExecutor():
    def __init__(
        self,
        textual_workflow: str,
        process_modell: WorkflowProcessor,
    ):
        self.repository = Repository()
        self.textual_workflow = textual_workflow
        self.logs = ""
        self.output_storage = []
        self.process_modell = process_modell 
        self.selector = FunctionSelector(self.repository)
        self.assignator = ParameterAssignator(self.repository)
        self.connection = OpenAIConnection()

    def _execute_exlusive_gateway(self, node:ExclusiveGateway, output:str) -> Node:
        node_2_condition = {
            n[0]: n[1] for n in self.process_modell.get_target_nodes(node)
        }
        condition_2_node = {c: n for n, c in node_2_condition.items()}
        conditions = [c for c in condition_2_node]

        sys_message = {"role": "system", "content": get_sys_message()}
        prompt = {
            "role": "user",
            "content": get_prompt(node.name, conditions, output)
        } 
        message = [sys_message, prompt]
        response = self.connection.request(message)

        DICT_PATTERN = r"{(.*?)}"
        ERROR_PATTERN = r"Condition error"
        if re.search(ERROR_PATTERN, response, re.IGNORECASE):
            raise Exception(
                f"Condition error - No condition can be chosen for '{node.name}'"
            )
        elif re.search(DICT_PATTERN, response, re.DOTALL):
            match = re.search(DICT_PATTERN, response, re.DOTALL).group()
            target_condition = json.loads(match)
            assert len(target_condition) == 1, (
                "Multiple conditions selected - Only one condition can be selected"
            ) 
            target_condition = str(list(target_condition.values())[0])
            target_node = condition_2_node[target_condition]
            self._provide_logging(f"Condition is selected: {target_condition}")

            return target_node
        else:
            raise Exception(
                "Neither an condition error nor a target node could be chosen - Please try again!"
            )
    
    def _execute_task(self, node:Task, output:str) -> Tuple[Node, str]:
        interface = self.selector.select(node, self.textual_workflow)
        arguments = self.assignator.assign(
            interface,
            self.textual_workflow,
            self.output_storage
        )
        self._provide_logging(f"{interface} is selected with arguments: {arguments}")

        try:
            output = self.repository.retrieve_interface(interface)(**arguments)
        except Exception as e:
            raise(f"Execution of the function failed with the error: {e}")
        self._provide_logging(f"Output of the function: {output}")
        self.output_storage.append({interface: output})
        target_node = self.process_modell.get_target_node(node)
        return (target_node, output)
    
    def _iterate_workflow(self, current_node:Node, output:str) -> None:
        while True:
            if self.process_modell.is_start_event(current_node):
                self._provide_logging("Process execution started")
                current_node = self.process_modell.get_target_node(current_node)
            elif self.process_modell.is_task(current_node):
                self._provide_logging(f"Execution of task: {current_node.get_name()}")
                current_node, output = self._execute_task(current_node, output)
            elif self.process_modell.is_exclusive_gateway(current_node):
                self._provide_logging(f"Execution of exclusive gateway: {current_node.get_name()}")
                current_node = self._execute_exlusive_gateway(current_node, output)
            elif self.process_modell.is_parallel_gateway(current_node):
                target_nodes = [n[0] for n in self.process_modell.get_target_nodes(current_node)]
                self._provide_logging("Parallelity started")
                for node in target_nodes:
                    self._iterate_workflow(node, output)
                self._provide_logging("Parallelity ended")
                break
            elif self.process_modell.is_end_event(current_node):
                self._provide_logging("Process execution ended")
                break

    def _provide_logging(self, text:str) -> None:
        self.logs += text + "\n"
        print(text)

    def run(self) -> None:        
        current_node = self.process_modell.get_start_node()
        output = ""
        self._iterate_workflow(current_node, output)

    def get_log(self)->str:
        return self.logs           