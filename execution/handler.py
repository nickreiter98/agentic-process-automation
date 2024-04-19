from typing import Optional
from misc import decoder

from openai import OpenAI

from execution import prompts_selection, prompts_arguments

import openai
import os
import logging
import json
import misc


class FunctionSelector:
    def __init__(
            self,
            # workflow_description,
            functions: Optional[list],
            model = 'gpt-3.5-turbo'
            
    ):
        # self.workflow_description = workflow_description
        self.model = model
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        self.chat_history = [{'role': 'system', 'content': prompts_selection.get_sys_message(self._parse_functions(functions))}]
        self.functions = self._parse_functions(functions)

    def _parse_functions(self, functions: Optional[list]) -> Optional[list]:
        if functions is None:
            return None
        return [decoder.func_to_json(func) for func in functions]
    

    def select(self, sub_process:str, workflow_description:str):
        self.chat_history.append({'role': 'user', 'content': prompts_selection.get_prompt(sub_process, workflow_description)})
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

    def assign(self, function:str, output, workflow:str):
        self.chat_history.append({'role': 'user', 'content': prompts_arguments.get_prompt(function, workflow, str(output))})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.chat_history
        )
        return response.choices[0].message.content


    
        


# sys_message = """
# You are executing single tasks of a process workflow given its input.
# You are precise and know the exact task you are executing.
# The tasks has been already extracted from the workflow.
# If the input is in accordance to the argument, dont chage the input, otherwise derive the argument from the input.
# """

# content = """
# current task:
# {}
# The input from the previous task:
# {}
# """


# class Agent:
#     def __init__(
#         self,
#         model: str = 'gpt-4',
#         functions: Optional[list] = None
#     ):
#         self.model = model
#         self.functions = self._parse_functions(functions)
#         self.func_mapping = self._create_func_mapping(functions)
#         self.chat_history = [{'role': 'system', 'content': sys_message}]
#         self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

#     def _parse_functions(self, functions: Optional[list]) -> Optional[list]:
#         if functions is None:
#             return None
#         return [decoder.func_to_json(func) for func in functions]

#     def _create_func_mapping(self, functions: Optional[list]) -> dict:
#         if functions is None:
#             return {}
#         return {func.__name__: func for func in functions}

#     def execute_function_call(self, task:str, input:str):
#         self.chat_history.append({'role': 'user', 'content': content.format(task, input)})

#         response = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=self.chat_history,
#                 functions=self.functions
#             )
        
#         func_name = response.choices[0].message.function_call.name
#         args_str = response.choices[0].message.function_call.arguments

#         args = json.loads(args_str)
#         func = self.func_mapping[func_name]
#         func_result =  func(**args)

#         # del(self.chat_history[-1])
#         return func_result
    
#     def get_function(self, task:str, input:str):
#         self.chat_history.append({'role': 'user', 'content': content.format(task, input)})

#         response = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=self.chat_history,
#                 functions=self.functions
#             )
        
#         func_name = response.choices[0].message.function_call.name
#         args_str = response.choices[0].message.function_call.arguments

#         args = json.loads(args_str)
#         func = self.func_mapping[func_name]
#         func_result =  func(**args)

#         # del(self.chat_history[-1])
#         return func