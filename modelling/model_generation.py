from modelling.generator import ModelGenerator
from openai import OpenAI
from modelling.code_extraction import extract_final_python_code
import modelling.workflow_prompt
import modelling.generator




# class TextToModel:
#     def __init__(self):
#         self.client = OpenAI()
#         self.process_model = None

#     def run(self, description:str):
#         prompt = modelling.workflow_prompt.create_model_generation_prompt(description)

#         response = self.client.chat.completions.create(
#             model='gpt-4',
#             messages=[
#                 {'role': 'user', 'content': prompt}
#             ]
#         )

#         response = response.choices[0].message.content
#         executable_code = extract_final_python_code(response)
#         local_vars = {}
#         exec(executable_code, globals(), local_vars)

#         self.process_model = local_vars['model']

#     def get_iterable_graph(self):
#         return self.process_model.get_iterable_graph()
    
#     def display_graph(self):
#         self.process_model.display_graph()
#         def save_graph(self, filename):
#             self.process_model.save_graph(filename)

def generate_model(description:str): 
    client = OpenAI()

    prompt = modelling.workflow_prompt.create_model_generation_prompt(description)

    response = client.chat.completions.create(
        model='gpt-4',
        messages=[
            {'role': 'user', 'content': prompt}
        ]
    )

    response = response.choices[0].message.content
    executable_code = extract_final_python_code(response)
    local_vars = {}
    exec(executable_code, globals(), local_vars)

    return local_vars['model']
