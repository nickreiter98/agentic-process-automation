import json
import re
import json

from pm4py.objects.bpmn.obj import BPMN
from src.registry.registry import Registry
from src.execution.task import FunctionSelector, ParameterAssignator
from src.execution.prompt_exclusive_gateway import get_sys_message, get_prompt
from src.modeling.process_processor import ProcessProcessor
from src.utils.open_ai import OpenAIConnection
from src.utils.errors import FunctionError, DecisionMakingError

from typing import Tuple, TypeAlias
StartEvent: TypeAlias = BPMN.StartEvent
EndEvent: TypeAlias = BPMN.EndEvent
Task: TypeAlias = BPMN.Task
ExclusiveGateway: TypeAlias = BPMN.ExclusiveGateway
ParallelGateway: TypeAlias = BPMN.ParallelGateway
Node: TypeAlias = BPMN.BPMNNode
Edge: TypeAlias = BPMN.Flow

# TODO: Check and probably change the use of output and data_cache
    
class ProcessExecutor():
    def __init__(self, textual_workflow: str, process_processor: ProcessProcessor):
        self.registry = Registry()
        self.textual_workflow = textual_workflow
        self.logs = ""
        self.data_cache = []
        self.process_processor = process_processor 
        self.selector = FunctionSelector(self.registry)
        self.assignator = ParameterAssignator(self.registry)
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

        target_nodes = self.process_processor.get_target_nodes(gateway)
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
            "content": get_prompt(gateway.name, conditions, self.data_cache)
        } 
        message = [sys_message, prompt]
        # Request the LLM to select the condition - dynamic decision making
        response = self.llm_connection.request(message)
        print(response)
        if re.search(ERROR_PATTERN, response, re.IGNORECASE):
            raise DecisionMakingError(
                f"No condition can be chosen for '{gateway.name}'"
            )
        elif re.search(DICT_PATTERN, response, re.DOTALL):
            # Extract the selected condition
            match = re.search(DICT_PATTERN, response, re.DOTALL).group()
            # Convert the condition to a dictionary
            target_condition = json.loads(match)
            # Check if only one condition is selected
            if len(target_condition) != 1:
                raise DecisionMakingError(
                    f"Multiple conditions selected for '{gateway.name}' "
                    f"- Only one condition can be selected"
                )
            # Get the selected condition
            target_condition = str(list(target_condition.values())[0])
            # Get the target node of the selected condition
            target_node = condition_2_node[target_condition]
            self._provide_logging(f"Condition is selected: {target_condition}")
            return target_node
        else:
            raise DecisionMakingError(f"Unkown error for '{gateway.name}'")
    
    def _execute_task(self, task:Task, output:str) -> Tuple[Node, str]:
        """Execute the task. 
        Contains the selection of the connector and the assignment of the parameters.

        :param task: task to be executed
        :param output: output of the previous task
        :return: target node of the task and the output of the task
        """
        # Select the connector which corresponds to the task
        connector= self.selector.select(task)
        # Assign the parameters of the connector
        arguments = self.assignator.assign(
            connector,
            self.textual_workflow,
            self.data_cache
        )
        self._provide_logging(f"{connector} is selected with arguments: {arguments}")

        try:
            # Execute the connector with the arguments
            output = self.registry.retrieve_connector(connector)(**arguments)
        except Exception as e:
            raise FunctionError(f"connector {connector} throws {e}")
        self._provide_logging(f"Output of the function: {output}")
        # add output to global output storage
        self.data_cache.append({connector: output})
        # Get the target node of the task
        target_node = self.process_processor.get_target_node(task)
        return (target_node, output)
    
    def _navigate_process(self, current_node:Node, output:str) -> None:
        """Iterate through the workflow. Designed to be recursive.

        :param current_node: current node which is inspected
        :param output: output of the previous task
        """
        while True:
            if self.process_processor.is_start_event(current_node):
                self._provide_logging("Process execution started")
                current_node = self.process_processor.get_target_node(current_node)
            elif self.process_processor.is_task(current_node):
                self._provide_logging(f"Execution of task: {current_node.get_name()}")
                current_node, output = self._execute_task(current_node, output)
            elif self.process_processor.is_exclusive_gateway(current_node):
                self._provide_logging(f"Execution of exclusive gateway: {current_node.get_name()}")
                current_node = self._execute_exlusive_gateway(current_node, output)
            elif self.process_processor.is_parallel_gateway(current_node):
                target_nodes = self.process_processor.get_target_nodes(current_node)
                target_nodes = [n[0] for n in target_nodes]
                self._provide_logging("Parallelity started")
                # Iterate through the target nodes of the parallel gateway
                for node in target_nodes:
                    # Calle the target node recursively
                    self._navigate_process(node, output)
                self._provide_logging("Parallelity ended")
                break
            elif self.process_processor.is_end_event(current_node):
                self._provide_logging("Process execution ended")
                break

    def _provide_logging(self, text:str) -> None:
        self.logs += f"{text}\n"
        print(text)

    def run(self) -> None:
        """Start the execution of the workflow
        """
        # Get start event to start the process      
        current_node = self.process_processor.get_start_node()
        # Start event doesnt possess any output
        output = ""
        self._navigate_process(current_node, output)

    def get_log(self)->str:
        return self.logs           