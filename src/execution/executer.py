import json
import re
import json

from pm4py.objects.bpmn.obj import BPMN
from src.repository.repository import Repository
from src.execution.handler import FunctionSelector, ParameterAssignator
from src.execution.prompt_exclusive_gateway import get_sys_message, get_prompt
from src.modelling.workflow_processor import WorkflowProcessor
from src.utils.open_ai import OpenAIConnection

from typing import Tuple, TypeAlias
StartEvent: TypeAlias = BPMN.StartEvent
EndEvent: TypeAlias = BPMN.EndEvent
Task: TypeAlias = BPMN.Task
ExclusiveGateway: TypeAlias = BPMN.ExclusiveGateway
ParallelGateway: TypeAlias = BPMN.ParallelGateway
Node: TypeAlias = BPMN.BPMNNode
Edge: TypeAlias = BPMN.Flow

# TODO: Check and probably change the use of output and output_storage
    
class WorkflowExecutor():
    def __init__(self, textual_workflow: str, process_modell: WorkflowProcessor):
        self.repository = Repository()
        self.textual_workflow = textual_workflow
        self.logs = ""
        self.output_storage = []
        self.process_modell = process_modell 
        self.selector = FunctionSelector(self.repository)
        self.assignator = ParameterAssignator(self.repository)
        self.llm_connection = OpenAIConnection()

    def _execute_exlusive_gateway(self, gateway:ExclusiveGateway, output:str) -> Node:
        """Execute the exclusive gateway.
        This includes also dynamic condition selection with the help of the LLM.

        :param gateway: exclusive gateway to be executed
        :param output: output of the previous task
        :raises Exception: If no condition can be chosen for the gateway
        :raises Exception: If multiple conditions are selected
        :raises Exception: Random error
        :return: target node of the exclusive gateway after the condition is selected
        """
        DICT_PATTERN = r"{(.*?)}"
        ERROR_PATTERN = r"Condition error"

        target_nodes = self.process_modell.get_target_nodes(gateway)
        # Create a dictionary with the node as key and the condition as value
        node_2_condition = {n[0]: n[1] for n in target_nodes}
        # Create a dictionary with the condition as key and the node as value
        condition_2_node = {c: n for n, c in node_2_condition.items()}
        # Get the conditions of the gateway
        conditions = [c for c in condition_2_node]

        # Create the prompts
        sys_message = {"role": "system", "content": get_sys_message()}
        prompt = {
            "role": "user",
            "content": get_prompt(gateway.name, conditions, output)
        } 
        message = [sys_message, prompt]
        # Request the LLM to select the condition - dynamic decision making
        response = self.llm_connection.request(message)

        if re.search(ERROR_PATTERN, response, re.IGNORECASE):
            raise Exception(
                f"Condition error - No condition can be chosen for '{gateway.name}'"
            )
        elif re.search(DICT_PATTERN, response, re.DOTALL):
            # Extract the selected condition
            match = re.search(DICT_PATTERN, response, re.DOTALL).group()
            # Convert the condition to a dictionary
            target_condition = json.loads(match)
            # Check if only one condition is selected
            if len(target_condition) != 1:
                raise Exception(
                    f"Multiple conditions selected '{gateway.name}' "
                    f"- Only one condition can be selected"
                )
            # Get the selected condition
            target_condition = str(list(target_condition.values())[0])
            # Get the target node of the selected condition
            target_node = condition_2_node[target_condition]
            self._provide_logging(f"Condition is selected: {target_condition}")
            return target_node
        else:
            raise Exception(
                "Neither an condition error nor a target node could be chosen - Please try again!"
            )
    
    def _execute_task(self, task:Task, output:str) -> Tuple[Node, str]:
        """Execute the task. 
        Contains the selection of the interface and the assignment of the parameters.

        :param task: task to be executed
        :param output: output of the previous task
        :return: target node of the task and the output of the task
        """
        # Select the interface which corresponds to the task
        interface = self.selector.select(task)
        # Assign the parameters of the interface
        arguments = self.assignator.assign(
            interface,
            self.textual_workflow,
            self.output_storage
        )
        self._provide_logging(f"{interface} is selected with arguments: {arguments}")

        try:
            # Execute the interface with the arguments
            output = self.repository.retrieve_interface(interface)(**arguments)
        except Exception as e:
            raise(f"Execution of the function failed with the error: {e}")
        self._provide_logging(f"Output of the function: {output}")
        # add output to global output storage
        self.output_storage.append({interface: output})
        # Get the target node of the task
        target_node = self.process_modell.get_target_node(task)
        return (target_node, output)
    
    def _iterate_workflow(self, current_node:Node, output:str) -> None:
        """Iterate through the workflow. Designed to be recursive.

        :param current_node: current node which is inspected
        :param output: output of the previous task
        """
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
                target_nodes = self.process_modell.get_target_nodes(current_node)
                target_nodes = [n[0] for n in target_nodes]
                self._provide_logging("Parallelity started")
                # Iterate through the target nodes of the parallel gateway
                for node in target_nodes:
                    # Calle the target node recursively
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
        """Start the execution of the workflow
        """
        # Get start event to start the process      
        current_node = self.process_modell.get_start_node()
        # Start event doesnt possess any output
        output = ""
        self._iterate_workflow(current_node, output)

    def get_log(self)->str:
        return self.logs           