import os
import json
import re

from src.utils.open_ai import OpenAIConnection
from src.execution import prompt_arguments, prompt_selection
from src.repository.repository import Repository

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
            repository: Repository,
            
    ):
        self.connection = OpenAIConnection()
        self.repository = repository

    def select(self, node:Node, workflow:str) -> str:
        sys_message = {'role': 'system',
                       'content': prompt_selection.get_sys_message(self.repository.get_function_to_json())}
        prompt = {'role': 'user',
                  'content': prompt_selection.get_prompt(node)}
        message = [sys_message, prompt]
        response = self.connection.request(message)
        DICT_PATTERN = r'{(.*?)}'
        ERROR_PATTERN = r'Selection error'
        if re.search(ERROR_PATTERN, response, re.IGNORECASE):
            raise Exception(f'Mapping error - No function can be mapped to the activity "{node.name}"')
        elif re.search(DICT_PATTERN, response, re.DOTALL):
            match = re.search(DICT_PATTERN, response, re.DOTALL).group()
            function_name = json.loads(match)
            assert len(function_name) == 1, ("Multiple functions selected -"
                                             " Only one function can be selected") 
            return list(function_name.values())[0]
        else:
            raise Exception("Neither an assignation error nor arguments could be detected"
                            " within the response. Please try again!")

class ParameterAssignator:
    def __init__(
            self,
            repository: Repository,
    ):
         self.connection = OpenAIConnection()
         self.repository = repository

    def assign(self, function_name:str, workflow:str, output_storage) -> str:
        sys_message = {'role': 'system', 
                       'content': prompt_arguments.get_sys_message()}
        prompt = {'role': 'user', 
                  'content': prompt_arguments.get_prompt(self.repository.get_json_by_name(function_name),
                                                          workflow,
                                                          output_storage)}
        message = [sys_message, prompt]
        response = self.connection.request(message)

        DICT_PATTERN = r'{(.*?)}'
        ERROR_PATTERN = r'Assignation error'
        if re.search(ERROR_PATTERN, response, re.IGNORECASE):
            raise Exception(f'Assignation error - No parameters can be assigned to the function "{function_name}"')
        elif re.search(DICT_PATTERN, response, re.DOTALL):
            match = re.search(DICT_PATTERN, response, re.DOTALL).group()
            arguments = json.loads(match)
            return arguments
        else:
            raise Exception("Neither an assignation error nor arguments could be detected"
                            " within the response. Please try again!")