from typing import Optional
from misc import decoder

from openai import OpenAI

import openai
import os
import logging
import json
sys_message = """
You are executing single tasks of a process workflow given its input.
You are precise and know the exact task you are executing.
The tasks has been already extracted from the workflow.
If the input is in accordance to the argument, dont chage the input, otherwise derive the argument from the input.
"""

content = """
current task:
{}
The input from the previous task:
{}
"""


class Agent:
    def __init__(
        self,
        model: str = 'gpt-4',
        functions: Optional[list] = None
    ):
        self.model = model
        self.functions = self._parse_functions(functions)
        self.func_mapping = self._create_func_mapping(functions)
        self.chat_history = [{'role': 'system', 'content': sys_message}]
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def _parse_functions(self, functions: Optional[list]) -> Optional[list]:
        if functions is None:
            return None
        return [decoder.func_to_json(func) for func in functions]

    def _create_func_mapping(self, functions: Optional[list]) -> dict:
        if functions is None:
            return {}
        return {func.__name__: func for func in functions}

    # def _generate_response(self) -> openai.ChatCompletion:
    #     print('.', end='')
    #     response = self._create_chat_completion(self.chat_history)
    #     result = self._handle_function_call(response)

    #     # if result is not None:
    #     #     self.chat_history.append({'role': 'assistant', 'content': f'{result}'})
    #     #     result = self._create_chat_completion(self.chat_history, use_functions=False)
        
    #     return result

    # def _create_chat_completion(
    #     self, messages: list, use_functions: bool=True
    # ) -> openai.OpenAI:
    #     if use_functions and self.functions:
    #         res = self.client.chat.completions.create(
    #             model=self.model,
    #             messages=messages,
    #             functions=self.functions
    #         )
    #     return res
        

    # def _handle_function_call(self, res: openai.ChatCompletion):
    #     #self.internal_thoughts.append(res.choices[0].message.dict())
    #     func_name = res.choices[0].message.function_call.name
    #     args_str = res.choices[0].message.function_call.arguments
    #     call_result = self._call_function(func_name, args_str)
    #     return call_result
        

    # def _call_function(self, func_name: str, args_str: str):
    #     args = json.loads(args_str)
    #     func = self.func_mapping[func_name]
    #     func_result =  func(**args)
    #     return func_result
        

    # def ask(self, workflow: str, task:str, input:str) -> openai.ChatCompletion:
    #     self.chat_history.append({'role': 'user', 'content': content.format(task, input)})
    #     res = self._generate_response()
    #     del(self.chat_history[-1])
    #     return res

    def execute_function_call(self, task:str, input:str):
        self.chat_history.append({'role': 'user', 'content': content.format(task, input)})

        response = self.client.chat.completions.create(
                model=self.model,
                messages=self.chat_history,
                functions=self.functions
            )
        
        func_name = response.choices[0].message.function_call.name
        args_str = response.choices[0].message.function_call.arguments

        args = json.loads(args_str)
        func = self.func_mapping[func_name]
        func_result =  func(**args)

        # del(self.chat_history[-1])
        return func_result

        