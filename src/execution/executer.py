import os
import json
import logging
import re
import json
import multiprocessing

from openai import OpenAI
from pm4py.objects.bpmn.obj import BPMN

from src.repository.repository import Repository
from src.execution.handler import FunctionSelector, ParameterAssignator
from src.execution.prompts_exclusive_gateway import get_sys_message, get_prompt
from src.modelling.generator import ModelGenerator
from src.utils.open_ai import OpenAIConnection

# Define type hints
from typing import List, Dict, Tuple, TypeAlias, Callable
StartEvent: TypeAlias = BPMN.StartEvent
EndEvent: TypeAlias = BPMN.EndEvent
Task: TypeAlias = BPMN.Task
ExclusiveGateway: TypeAlias = BPMN.ExclusiveGateway
ParallelGateway: TypeAlias = BPMN.ParallelGateway
Node: TypeAlias = BPMN.BPMNNode
Edge: TypeAlias = BPMN.Flow
    
class Executor():
    def __init__(
        self,
        workflow: str,
        process_modell: ModelGenerator,
    ):
        self.list_functions = self._get_functions_from_repository()
        self.name_2_function = self._map_name_to_function(self.list_functions)
        self.workflow = workflow
        self.process_modell = process_modell 
        self.selector = FunctionSelector(functions=self.list_functions)
        self.assignator = ParameterAssignator(functions=self.list_functions)
        self.connection = OpenAIConnection()
        
    def _get_functions_from_repository(self) -> List[Callable]:
        return Repository().functions
    
    def _map_name_to_function(self, functions:List[Callable]) -> Dict[str,Callable]:
        if functions is None:
            return {}
        return {func.__name__: func for func in functions}

    def _execute_exlusive_gateway(self, node:ExclusiveGateway, output:str) -> Node:
        node_2_condition = {n[0]: n[1] for n in self.process_modell.get_target_nodes(node)}
        condition_2_node = {c: n for n, c in node_2_condition.items()}
        conditions = [c for c in condition_2_node]

        sys_message = {'role': 'system', 'content': get_sys_message()}
        prompt = {'role': 'user', 'content': get_prompt(node.name, conditions, output)} 
        message = [sys_message, prompt]
        response = self.connection.request(message)

        try:
            response = json.loads(response)
        except Exception:
            raise Exception('Selection of condition failed - Please try again')
        
        if len(response) > 1:
            raise Exception('Multiple conditions selected - Only one condition can be selected')
        else:
            target_condition = str(list(response.values())[0])
        
        if re.findall('\bNO CONDITION FOUND\b', target_condition, re.IGNORECASE):
            raise Exception('No condition selected - No condition can be mapped to the activity')
        else:
            target_node = condition_2_node[target_condition]

        logging.info(f'Condition is selected: {target_condition}')
        return target_node
    
    def _execute_task(self, node:Task, output:str) -> Tuple[Node, str]:
        function_name = self.selector.select(node, self.workflow)
        arguments = self.assignator.assign(function_name, output, self.workflow)
        logging.info(f'{function_name} is selected with arguments: {arguments}')
        arguments = json.loads(arguments)
        try:
            output = self.name_2_function[function_name](**arguments)
        except Exception as e:
            raise(f'Execution of interface function from the repository failed: {e}')
        
        target_node = self.process_modell.get_target_node(node)
        return (target_node, output)
    
    def _check_node_for_execution(self, current_node:Node, output:str) -> None:
        while True:
            if self.process_modell.is_start_event(current_node):
                logging.info('Process started')
                current_node = self.process_modell.get_target_node(current_node)
            elif self.process_modell.is_task(current_node):
                logging.info(f'Execution of task: {current_node.get_name()}')
                current_node, output = self._execute_task(current_node, output)
            elif self.process_modell.is_exclusive_gateway(current_node):
                logging.info(f'Execution of parallel gateway: {current_node.get_name()}')
                current_node = self._execute_exlusive_gateway(current_node, output)
            elif self.process_modell.is_parallel_gateway(current_node):
                target_nodes = [n[0] for n in self.process_modell.get_target_nodes(current_node)]
                processes = []
                logging.info('Parallelity started')
                for node in target_nodes:
                    processes.append(multiprocessing.Process(target=self._check_node_for_execution, args=(node, output)))
                for process in processes:
                    process.start()
                for process in processes:
                    process.join()
                logging.info('Parallelity ended')
                break
            elif self.process_modell.is_end_event(current_node):
                logging.info('Process ended')
                break

    
    def run(self) -> None:        
        current_node = self.process_modell.get_start_node()
        output = ''

        self._check_node_for_execution(current_node, output)

        
                
                


            