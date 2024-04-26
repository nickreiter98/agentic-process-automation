import os
import json
import logging
import ast
import json
import multiprocessing

from openai import OpenAI
from pm4py.objects.bpmn.obj import BPMN

from repository.repository import Repository
from execution.handler import FunctionSelector, ParameterAssignator
from execution.prompts_exclusive_gateway import get_sys_message, get_prompt
from modelling.generator import AdjacentDict

f# Define type hints
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
        description: str,
        process_modell: AdjacentDict,
    ):
        self.function_list = self._get_functions_from_repository()
        self.func_mapping = self._map_name_to_function(self.function_list)
        self.description = description
        self.process_modell = process_modell 
        
    def _get_functions_from_repository(self) -> List[Callable]:
        return Repository().functions
    
    def _map_name_to_function(self, functions:List[Callable]) -> Dict[str:Callable]:
        if functions is None:
            return {}
        return {func.__name__: func for func in functions}

    def _execute_exlusive_gateway(self, node:ExclusiveGateway, output) -> Node:
        node_2_condition = {n[0]: n[1] for n in self.process_modell.get_target_nodes(node)}
        condition_2_node = {c: n for n, c in node_2_condition.items()}
        conditions = [node_2_condition[n] for n in node_2_condition]

        client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        chat_history = [{'role': 'system', 'content': get_sys_message()},
                        {'role': 'user', 'content': get_prompt(node.name, conditions, output)}]
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=chat_history
        )

        response = ast.literal_eval(response.choices[0].message.content)
        target_condition = str(list(response.values())[0])
        print(f'Following condition is executed: {target_condition}')
        target_node = condition_2_node[target_condition]

        return target_node
    
    def _execute_task(self, node:BPMN.Task, output) -> Tuple[Node, str]:
        selector = FunctionSelector(functions=self.function_list)
        assignator = ParameterAssignator(functions=self.function_list)

        function = selector.select(node, self.description)
        arguments = assignator.assign(function, output, self.description)
        arguments = json.loads(arguments)
        output = self.func_mapping[function](**arguments)
        target_node = self.process_modell.get_target_node(node)

        return (target_node, output)  
    
    
    def _check_node_for_execution(self, current_node:Node, output) -> None:
        while True:
            if self.process_modell.is_start_event(current_node):
                print('Process is started')
                current_node = self.process_modell.get_target_node(current_node)
            elif self.process_modell.is_task(current_node):
                print(f'Following node is executed: {current_node.get_name()}')
                current_node, output = self._execute_task(current_node, output)
            elif self.process_modell.is_exclusive_gateway(current_node):
                print(f'Following node is executed: {current_node.get_name()}')
                current_node = self._execute_exlusive_gateway(current_node, output)
            elif self.process_modell.is_parallel_gateway(current_node):
                target_nodes = [n[0] for n in self.process_modell.get_target_nodes(current_node)]
                processes = []
                print('Parallelity started')
                for node in target_nodes:
                    processes.append(multiprocessing.Process(target=self._check_node_for_execution, args=(node, output)))
                for process in processes:
                    process.start()
                for process in processes:
                    process.join()
                print('Parallelity ended')
                break
            elif self.process_modell.is_end_event(current_node):
                print('Process is ended')
                break

    
    def run(self) -> None:        
        current_node = self.process_modell.get_start_node()
        output = ''

        self._check_node_for_execution(current_node, output)

        
                
                


            