import traceback
import logging
from openai import OpenAI

from src.modelling.code_extraction import extract_final_python_code
from src.modelling import workflow_prompt
from src.utils.open_ai import OpenAIConnection
from src.utils.output_redirection import _print

from typing import List, Dict

def generate_workflow(description:str, max_iteration:int = 5) -> str: 
    prompt = workflow_prompt.create_model_generation_prompt(description)
    messages = [{'role': 'user', 'content': prompt}]

    connection = OpenAIConnection()
    
    for i in range(max_iteration):
        try:
            logging.info(f'Iteration {i+1} of model generation')
            _print(f'Iteration {i+1} of model generation')
            response = connection.request(messages)
            messages.append({'role': 'system', 'content': response})
            executable_code = extract_final_python_code(response)
            with open('executabel_code.txt', 'w') as f:
                f.write(executable_code)
            local_vars = {}
            exec(executable_code, globals(), local_vars)
            logging.info('Model generation successful')
            _print('Model generation successful')
            return local_vars['model']
        except Exception as e:
            error_description = str(e)
            new_message = (f" Executing your code led to an error! Please update the model to fix the error."
                           f" This is the error message: {error_description}")
            logging.info(new_message)
            _print(f'{new_message}')
            messages.append({'role': 'user', 'content': new_message})