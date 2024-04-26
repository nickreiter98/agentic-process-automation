from openai import OpenAI
from misc.directed_graph import DirectedGraph
from execution.handler import FunctionSelector, ParameterAssignator
from execution.prompts_exclusive_gateway import get_sys_message, get_prompt
from misc import decoder

from modelling.notation import Node, Edge, ExclusiveEdge, StartEvent, EndEvent, Task, ExclusiveGateway, ParallelGateway
from modelling.generator import ModelGenerator

from repository.repository import Repository

from openai import OpenAI

import os
import json
import logging
import ast
import json

from typing import Callable

    
class Executor():
    def __init__(
        self,
        description: str,
        process_modell: ModelGenerator,
    ):
        self.function_list = self._get_functions_from_repository()
        self.func_mapping = self._map_name_to_function(self.function_list)
        self.description = description
        self.process_modell = process_modell 
        
    def _get_functions_from_repository(self):
        return Repository().functions
    
    def _map_name_to_function(self, functions:list[Callable]) -> dict[str:Callable]:
        if functions is None:
            return {}
        return {func.__name__: func for func in functions}

    def _execute_exlusive_gateway(self, node:ExclusiveGateway, output) -> Node:
        node_2_condition = self.process_modell.get_target_nodes_with_condition(node)
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
        trgt_cndt = str(list(response.values())[0])
        trgt_nd = condition_2_node[trgt_cndt]

        return trgt_nd
    
    def _execute_task(self, node:Task, output) -> Node:
        selector = FunctionSelector(functions=self.function_list)
        assignator = ParameterAssignator(functions=self.function_list)

        function = selector.select(node, self.description)
        arguments = assignator.assign(function, output, self.description)
        arguments = json.loads(arguments)
        output = self.func_mapping[function](**arguments)
        trgt_nd = self.process_modell.get_target_nodes(node)[0]

        return trgt_nd
    
    def run(self):        
        current_node = self.process_modell.get_start_node()
        output = ''

        while True:
            if isinstance(current_node, StartEvent):
                current_node = self.process_modell.get_target_nodes(current_node)[0]
            elif isinstance(current_node, Task):
                current_node = self._execute_task(current_node, output)
            elif isinstance(current_node, ExclusiveGateway):
                current_node = self._execute_exlusive_gateway(current_node, output)
            elif isinstance(current_node, EndEvent):
                break
                
                


            