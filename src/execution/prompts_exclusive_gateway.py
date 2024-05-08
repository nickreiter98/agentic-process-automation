def add_role():
    return  " Your role: imagine you are an exclusive gateway," \
            " and you are able to chose the right condition given data" \
            " to a specific context \n\n "

def add_least_to_most():
    return  " Select the right condition based on the given data." \
            " For this follow the upcoming steps:\n" \
            " - 1.: Read the data carefully and understand the context of the data to compare." \
            " - 2.: Compare the data with the conditions and chose the right condition." \
            " - 3.: If you cannot find the right condition, return an error message." \
            " - 4.: If you have found the right condition, return your findings\n\n"

def add_output_pattern():
    return  " Use the provided template below to return the output:\n" \
            " {\"name\": \"condition\"}\n" \
            " - condition: place holder for the name of the condition which is true\n" \
            " E.g. {\"name\": \"Bank account > 10000€\"}\n" \
            " E.g. {\"name\": \"message is spam\"}\n\n" \
            " If you were unsuccessfull chosing a function, return" \
            " {\"name\": \"NO CONDITION FOUND\"} \n\n"\
            
def get_sys_message():
    sys_message = add_role()
    sys_message += add_least_to_most()
    sys_message += add_output_pattern()
    return sys_message

def get_prompt(context:str, conditions:list[str], output:str):
    prompt =    f" Chose the right condition based on the given data and cobtext. \n\n" \
                f" Data: {output}" \
                f" Context: {context} \n\n"
    
    for i, condition in  enumerate(conditions):
        prompt += f" - Condition {i+1}: {condition} \n"
                
    return prompt