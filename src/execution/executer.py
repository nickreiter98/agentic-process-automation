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

from src.utils.output_redirection import _print

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
        self.repository = Repository()
        self.workflow = workflow
        self.logs = ''
        self.output_storage = []
        self.process_modell = process_modell 
        self.selector = FunctionSelector(repository=self.repository)
        self.assignator = ParameterAssignator(repository=self.repository)
        self.connection = OpenAIConnection()

    def _execute_exlusive_gateway(self, node:ExclusiveGateway, output:str) -> Node:
        node_2_condition = {n[0]: n[1] for n in self.process_modell.get_target_nodes(node)}
        condition_2_node = {c: n for n, c in node_2_condition.items()}
        conditions = [c for c in condition_2_node]

        sys_message = {'role': 'system', 'content': get_sys_message()}
        prompt = {'role': 'user', 'content': get_prompt(node.name, conditions, output)} 
        message = [sys_message, prompt]
        response = self.connection.request(message)

        DICT_PATTERN = r'{(.*?)}'
        ERROR_PATTERN = r'Condition error'
        if re.search(ERROR_PATTERN, response, re.IGNORECASE):
            raise Exception(f'Condition error - No condition can be chosen for "{node.name}"')
        elif re.search(DICT_PATTERN, response, re.DOTALL):
            match = re.search(DICT_PATTERN, response, re.DOTALL).group()
            target_condition = json.loads(match)
            assert len(target_condition) == 1, ("Multiple conditions selected -"
                                                " Only one condition can be selected") 
            target_condition = str(list(target_condition.values())[0])
            target_node = condition_2_node[target_condition]
            logging.info(f'Condition is selected: {target_condition}')
            self.logs += f'Condition is selected: {target_condition}\n'
            _print(f'Condition is selected: {target_condition}')

            return target_node
        else:
            raise Exception("Neither an condition error nor the function could be mapped"
                            " Please try again!")
    
    def _execute_task(self, node:Task, output:str) -> Tuple[Node, str]:
        function_name = self.selector.select(node, self.workflow)
        arguments = self.assignator.assign(function_name, self.workflow, self.output_storage )
        logging.info(f'{function_name} is selected with arguments: {arguments}')
        self.logs += f'{function_name} is selected with arguments: {arguments}\n'
        _print(f'{function_name} is selected with arguments: {arguments}')

        try:
            output = self.repository.get_function_by_name(function_name)(**arguments)
        except Exception as e:
            raise(f'Execution of the function failed with the error: {e}')
        
        self.output_storage.append({function_name: output})
        self.logs += f'Output of the function: {output}\n'
        _print(f'Output of the function: {output}')
        target_node = self.process_modell.get_target_node(node)
        return (target_node, output)
    
    def _run_execution(self, current_node:Node, output:str) -> None:
        while True:
            if self.process_modell.is_start_event(current_node):
                logging.info('Process started')
                self.logs += 'Process started\n'
                _print('Process started')
                current_node = self.process_modell.get_target_node(current_node)
            elif self.process_modell.is_task(current_node):
                logging.info(f'Execution of task: {current_node.get_name()}')
                self.logs += f'Execution of task: {current_node.get_name()}\n'
                _print(f'Execution of task: {current_node.get_name()}')
                current_node, output = self._execute_task(current_node, output)
            elif self.process_modell.is_exclusive_gateway(current_node):
                logging.info(f'Execution of parallel gateway: {current_node.get_name()}')
                self.logs += f'Execution of parallel gateway: {current_node.get_name()}\n'
                _print(f'Execution of parallel gateway: {current_node.get_name()}')
                current_node = self._execute_exlusive_gateway(current_node, output)
            elif self.process_modell.is_parallel_gateway(current_node):
                target_nodes = [n[0] for n in self.process_modell.get_target_nodes(current_node)]
                processes = []
                logging.info('Parallelity started')
                self.logs += 'Parallelity started\n'
                _print('Parallelity started')
                for node in target_nodes:
                    self._run_execution(node, output)
                # for node in target_nodes:
                #     processes.append(multiprocessing.Process(target=self._run_execution, args=(node, output)))
                # for process in processes:
                #     process.start()
                # for process in processes:
                #     process.join()
                logging.info('Parallelity ended')
                self.logs += 'Parallelity ended\n'
                _print('Parallelity ended')
                break
            elif self.process_modell.is_end_event(current_node):
                logging.info('Process ended')
                self.logs += 'Process ended\n'
                _print('Process ended')
                break

    def run(self) -> None:        
        current_node = self.process_modell.get_start_node()
        output = ''
        self._run_execution(current_node, output)

    def get_log(self)->str:
        return self.logs           