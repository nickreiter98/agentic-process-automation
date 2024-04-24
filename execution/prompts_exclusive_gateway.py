def add_role():
    return  " Your role: imagine you are an exclusive gateway," \
            " and you are able to chose the right condition." \
            " Your task is to chose the right branch respectice the condition which is true" \
            " You compare the condition against some provided data" \
            " When selecting the branch/condition, be as precise as possible.\n\n"

def add_exact_task():
    return  " Your Task is: Chose the condition which is true provided the given data" \
            " and return only the condtition itself as a dictioanry" \
            " in the format: {'Number of condition': 'condition itself'}" \
            " e.g {'Condition 3': 'Account > 100€'}" \
            " You are provided a task which signifies the overall task and the conditions" \
            " The conditions can be of mathematical or logical nature"


def get_sys_message():
    sys_message = add_role()
    sys_message += add_exact_task()
    return sys_message

def get_prompt(task:str, conditions:list[str], output:str):
    prompt =    f" Chose the right based on the given data. \n\n" \
                f" Data: {output}" \
                f" Task: {task} \n\n"
    
    for i, condition in  enumerate(conditions):
        prompt += f" - Condition {i+1}: {condition} \n"
                
    return prompt