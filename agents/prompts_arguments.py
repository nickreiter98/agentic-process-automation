def add_role():
    return  " Your role: you are an expert in function calling," \
            " familiar with common function calling approaches." \
            " Your task is to assign parameters of a function with the right arguments" \
            " given the output of the previous function," \
            " the description of the function itself." \
            " and the context of a workflow from which the function has already been selected" \
            " When assigning the parameters, be as precise as possible" \
            " and capture all details from the"\
            " context from the workflow as well as the input from the previous function" \
            " Also act as the process owner and use" \
            " your expertise and familiarity with the" \
            " workflow process context to avoid any irrational assigments. \n\n"

def add_knowledge():
    return  " An parameter assignator refers to a mechanism or a process within a program" \
            " that assigns parameters of a function with arguments. A parameter assignator" \
            " contains following charactersitcs: \n " \
            " - Argument Extraction: The parameter assignator is responsible to extract" \
            " the arguments from the input of the previous function and the context" \
            " from the workflow. \n" \
            " - Value Assignment to Parameters: In function calls, parameters are" \
            " essentially variables defined in the function's signature that receive" \
            " values (arguments) passed when the function is called. A parameter assignator" \
            " is responsible for linking each passed argument to its corresponding" \
            " parameter in the function definition.\n" \
            " - Type and Value Validation: This charactersitc also includes checking" \
            " that the arguments provided match the expected types as declared" \
            " in the function’s parameters and performing type coercion if needed. \n" \
            " - Python as underlying programming language: The parameter" \
            " assignator is based on Python programming language and uses all" \
            " Python-specific mechanism for calling functions \n" \

def add_exact_task():
    return  " Your Task is: assign the parameters of the function with arguments" \
            " First at all only use the information from the output of" \
            " the previous function as arguments. If this is not possible, use the context from the workflow" \
            " Try to keep the arguments as close as possible to the output" \
            " E.g. output is a dict and only some key-value pairs of it are needed as arguments" \
            " then chose these two key-value pairs as arguments. \n" \
            " If you cannot directly derive the parameters from the context and output" \
            " of previous function. Use your knowledge about the process itself" \
            " Return the arguments of the function to be called in a dict as {\"argument\":\"parameter\"} and " \
            " don't forget to put arguments and parameters in double quotes" \
            " do not call the function itself. \n" \
            " Really impotant!!! only return the dict"

def add_errors():
    return '''Try to avoid the following errors:
            - OUTPUT:
            {'location': {'name': 'Berlin',
                'region': 'Berlin',
                'country': 'Germany',
                'lat': 52.52,
                'lon': 13.4,}
            }
            - FUNCTION: d_write_text
            - WORKFLOW: Get a random location and then write a text about its being.

            - OUTPUT: {'text_context': 'Berlin is the capital of Germany. It got a lot of history and is a great place to visit.',
                        'context_info': 'Informal, general information'}

            - ERROR: The output is a dict, but the argument of text_context has already been formulated.
            In this case, you are only providing the output for the function to be called.
            A possible solution might be: {'text_content': 'Berlin is in Germany and in the region of Berlin. It is located at lat 52.53 and lon 13.4',
                        'context_info': 'Informal, general information'}
        '''
def add_function_repository(function_repository:list[dict]):
    return  f" This is the function repository providing the function descriptions: \n" \
            f" {function_repository} "


def get_sys_message(function_repository:list[dict]):
    sys_message = add_role()
    sys_message += add_knowledge()
    sys_message += add_exact_task()
    sys_message += add_errors()
    sys_message += add_function_repository(function_repository)
    return sys_message

def get_prompt(function:str, workflow:str, output:str):
    prompt =    f" Assign the parmeter of provided function with appropriate argument." \
                f" The function to be assigned is: {function} \n"\
                f" The output from the previous function is: {output} \n" \
                f" The workflow description is: {workflow} \n"
    return prompt