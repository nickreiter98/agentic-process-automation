import os

from misc import decoder
from openai import OpenAI
from pm4py.objects.bpmn.obj import BPMN

from execution import prompts_selection, prompts_arguments

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
            model = 'gpt-3.5-turbo'
            
    ):
        self.model = model
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        self.functions = self._parse_functions(functions)
        self.chat_history = [{'role': 'system', 'content': prompts_selection.get_sys_message(self.functions)}]
        
    def _parse_functions(self, functions: Optional[list]) -> Optional[list]:
        if functions is None:
            return None
        return [decoder.func_to_json(func) for func in functions]

    def select(self, node:Node, description:str) -> str:
        self.chat_history.append({'role': 'user', 'content': prompts_selection.get_prompt(node.get_name(), description)})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.chat_history
        )
        return response.choices[0].message.content
    

class ParameterAssignator:
    def __init__(
            self,
            functions: Optional[list],
            model = 'gpt-3.5-turbo'
    ):
        self.model = model
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        self.chat_history = [{'role': 'system', 'content': prompts_arguments.get_sys_message(self._parse_functions(functions))}]
        self.functions = self._parse_functions(functions)

    def _parse_functions(self, functions: Optional[list]) -> Optional[list]:
        if functions is None:
            return None
        return [decoder.func_to_json(func) for func in functions]

    def assign(self, function:str, output:str, workflow:str) -> str:
        self.chat_history.append({'role': 'user', 'content': prompts_arguments.get_prompt(function, workflow, str(output))})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.chat_history
        )
        return response.choices[0].message.content
