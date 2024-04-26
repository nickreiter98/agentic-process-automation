from openai import OpenAI
from modelling.code_extraction import extract_final_python_code
import modelling.workflow_prompt
import modelling.generator

def generate_model(description:str) -> str: 
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
    with open('executabel_code.txt', 'w') as f:
        f.write(executable_code)
    local_vars = {}
    exec(executable_code, globals(), local_vars)

    return local_vars['model']
