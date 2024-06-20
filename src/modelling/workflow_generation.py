import traceback
import logging
from openai import OpenAI

from src.modelling.code_extraction import extract_final_python_code
from src.modelling import prompt_workflow
from src.utils.open_ai import OpenAIConnection

from typing import List, Dict

def generate_workflow(description:str, max_iteration:int = 5) -> str: 
    prompt = prompt_workflow.create_model_generation_prompt(description)
    messages = [{'role': 'user', 'content': prompt}]

    connection = OpenAIConnection()
    
    for i in range(max_iteration):
        try:
            print(f'Iteration {i+1} of model generation')
            response = connection.request(messages)
            messages.append({'role': 'system', 'content': response})
            executable_code = extract_final_python_code(response)
            # with open('executabel_code.txt', 'w') as f:
            #     f.write(executable_code)
            local_vars = {}
            exec(executable_code, globals(), local_vars)
            print('Model generation successful')
            return local_vars['model']
        except Exception as e:
            error_description = str(e)
            new_message = (f"Executing your code led to an error! "
                           f"Please update the model to fix the error. "
                           f"This is the error message: {error_description}")
            print(f'{new_message}')
            messages.append({'role': 'user', 'content': new_message})