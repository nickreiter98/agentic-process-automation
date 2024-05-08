def add_role():
    return  " You are an expert in function calling," \
            " familiar with common function calling approaches." \
            " Your task is to assign the parameters of a function with the right arguments" \
            " The arguments can be derived from the output of the prvious function and/or from a workflow description" \
            " Note, Previously activities from the workflow have been mapped to a function." \
            " Also act as the process owner and use your expertise and familiarity with the" \
            " workflow process context to avoid any irrational assigments. \n\n"

def add_knowledge():
    return  " An parameter assignator refers to a mechanism or a process within a program" \
            " that assigns parameters of a function with arguments. A parameter assignator" \
            " contains following charactersitcs: \n " \
            " - Argument Extraction: The process of identifying and extracting arguments or" \
            " parameters passed to a specific function. Also recognizes, if parameters are optional/required\n" \
            " - Type and Value Validation: The process of checking" \
            " that arguments provided match the expected types as declared" \
            " within the function description. Performing type coercion if needed. \n\n" \

def add_least_to_most():
    return  " Assign the parameters of the function with arguments." \
            " I will provide a step-by-step schedule:\n" \
            " - 1.: Assign the parameters of the function or some of them with the output of the previous function. Or with some parts of the output\n" \
            " - 2.: Assign the parameters which haven't been assigned yet with arguments extracted from the workflow description.\n"\
            " - 3.: If assignation is not possible, throw an Assignation error\n"\
            " In the cases decide whether optional arguments are needed or not."\
            " If you cannot assign the parameters, return an error message. \n\n" \

def add_errors():
    return '''Try to avoid the following errors:
            - OUTPUT:
            {'location': {'name': 'Berlin',
                'region': 'Berlin',
                'country': 'Germany',
                'lat': 52.52,
                'lon': 13.4,}
            }
            - WORKFLOW: Get a random location and then write a text about the location.

            - FUNCTION: d_write_text
            - INPUT: {'text_context': 'Berlin, the capital city of Germany, is a vibrant metropolis renowned for its cultural diversity, rich history, and dynamic art scene. This city is not just the political center of Germany but also a pivotal cultural hub in Europe, blending historical landmarks with modern, cutting-edge culture.',
                        'context_info': 'Informal, general information'}

            - ERROR: The output is a dict, but the argument of text_context has already been formulated.
            In this case, you are only providing the output for the function to be called.
            A possible solution might be: {'text_content': 'Berlin is in Germany and in the region of Berlin. It is located at lat 52.53 and lon 13.4',
                        'context_info': 'Informal, general information'}
        '''

def add_function_repository(function_repository:list[dict]):
    text = ("These are all functions from the function repository: \n"
            "++++++++++Start Function Repository++++++++++\n")
    
    for i, function in enumerate(function_repository):
        text += f"Function {i+1} --> {function} \n"

    text += "++++++++++End Function Repository++++++++++\n\n"
    return text

def add_output_pattern():
     return (" +++ TEMPLATE PATTERN +++\n" 
             " Use the provided template below to return the output: \n"
             " {\"parameter\": \"value\", \"parameter\": \"value\"} \n"
             " - parameter: place holder for the parameter to be assigned.\n"
             " - value: place holder for the value to be assigned to the parameter.\n\n"
             " +++ ERROR HANDLING +++\n"
             " - If you were unsuccessfull assigning, return:"
             " Assignation error \n")


def get_sys_message(function_repository:list[dict]):
    sys_message = add_role()
    sys_message += add_knowledge()
    sys_message += add_least_to_most()
    #sys_message += add_errors()
    sys_message += add_function_repository(function_repository)
    sys_message += add_output_pattern()
    return sys_message

def get_prompt(function:str, workflow:str, output:str):
    prompt =    f" Assign the parmeter of provided function with arguments.\n" \
                f" - Function arguments to be assigned: {function} \n"\
                f" - Output from the previous function: {output} \n" \
                f" - Workflow description: {workflow} \n\n"
    return prompt