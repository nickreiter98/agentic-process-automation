import os
import json
import re

from src.misc import decoder
from src.utils.open_ai import OpenAIConnection
from src.execution import prompts_selection, prompts_arguments

from openai import OpenAI
from pm4py.objects.bpmn.obj import BPMN

# Define type hints
from typing import Optional, TypeAlias
StartEvent: TypeAlias = BPMN.StartEvent
EndEvent: TypeAlias = BPMN.EndEvent
Task: TypeAlias = BPMN.Task
ExclusiveGateway: TypeAlias = BPMN.ExclusiveGateway
ParallelGateway: TypeAlias = BPMN.ParallelGateway
Node: TypeAlias = BPMN.BPMNNode
Edge: TypeAlias = BPMN.Flow
    
class FunctionSelector:
    def __init__(
            self,
            functions: Optional[list],
            
    ):
        self.connection = OpenAIConnection()
        self.list_parsed_functions = self._parse_functions(functions)
        
        
    def _parse_functions(self, functions: Optional[list]) -> Optional[list]:
        if functions is None:
            raise Exception('Empty function repository - please provide functions to select from')
        else:
            return [decoder.func_to_json(func) for func in functions]

    def select(self, node:Node, workflow:str) -> str:
        sys_message = {'role': 'system',
                        'content': prompts_selection.get_sys_message(self.list_parsed_functions)}
        prompt = {'role': 'user',
                   'content': prompts_selection.get_prompt(node, workflow)}
        
        message = [sys_message, prompt]
        response = self.connection.request(message)

        if re.search('\bSelection error\b', response, re.IGNORECASE):
            raise Exception('Mapping error - No function can be mapped to the activity')
        else:
            function_name = json.loads(response)

        # Probably this condition is never occuring
        if len(function_name) > 1:
            raise Exception('Multiple functions selected - Only one function can be selected') 
        else:
            return list(function_name.values())[0]
        
class ParameterAssignator:
    def __init__(
            self,
            functions: Optional[list],
    ):
         self.connection = OpenAIConnection()
         self.list_parsed_functions = self._parse_functions(functions)

    def _parse_functions(self, functions: Optional[list]) -> Optional[list]:
        if functions is None:
            return None
        return [decoder.func_to_json(func) for func in functions]

    def assign(self, function_name:str, output:str, workflow:str) -> str:
        sys_message = {'role': 'system', 
                       'content': prompts_arguments.get_sys_message(self.list_parsed_functions)}
        prompt = {'role': 'user', 
                  'content': prompts_arguments.get_prompt(function_name, workflow, str(output))}
        message = [sys_message, prompt]
        response = self.connection.request(message)

        DICT_PATTERN = r'{(.*?)}'
        ERROR_PATTERN = r'Assignation error'
        if re.search(ERROR_PATTERN, response, re.IGNORECASE):
            raise Exception('Assignation error - No parameters can be assigned to the function')
        elif re.search(DICT_PATTERN, response, re.DOTALL):
            match = re.search(DICT_PATTERN, response, re.DOTALL)
            return match.group()
        else:
            return response