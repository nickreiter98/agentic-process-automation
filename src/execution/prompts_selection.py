def add_role():
    return  " Your role: you are an expert in function calling," \
            " familiar with common function calling approaches." \
            " Your task is to map a sub-process/activity from a workflow description" \
            " to a function by selecting the function from a function collection" \
            " When selecting the function, be as precise as possible" \
            " and capture all details from the sub-process/activity as well as the"\
            " context from the workflow description in the function." \
            " Also act as the process owner and use" \
            " your expertise and familiarity with the" \
            " workflow process context to avoid any irrational selections. \n\n"

def add_knowledge():
    return  " Function calling is a powerful feature that significantly enhances the" \
            " capabilities of Large Language Models (LLMs). It enables better functionality," \
            " immediate data access and interaction, and sets up for integration with" \
            " external APIs and services. Function calling turns LLMs into adaptable" \
            " tools for various use case scenarios." \
            " Function calling enhances the capabilities of LLMs beyond just text" \
            " generation. It allows to convert human-generated prompts into precise function" \
            " invocation descriptors. These descriptors can then be used by connected LLM frameworks" \
            " to perform computations, manipulate data, and interact with external APIs."\
            " This expansion of functionality makes LLMs adaptable tools for a wide array"\
            " of tasks and industries. \n\n"

def add_least_to_most():
    return  " Your Task is: Chose the name of the function that best represents the sub-process/activity" \
            " and return only the name of the function nothing else." \
            " If you are unable to find a suitable function for the activity, return an error message. \n\n" \


# def add_role():
#     return  (" You are an expert in function calling, familiar with common function calling approaches." 
#             " Your task is to map an activity to a function by selecting the function"
#             " from a function collection\n\n")
            
            
# def add_least_to_most():
#     return  (" The function repository contains a collection of functions that can be mapped to an activity." 
#             " The function repository comes in a form of a list of dictionaries, where each dictionary." 
#             " contains the function name which is the key, and the value is"
#             " the function description and the function parameters." 
#             " I will provide a step-by-step schedule. If one step is not possible continuer with the next one:\n" 
#             " - 1.: select the appropriate function from the function repository by" 
#             " deriving it from the activity and context of workflow. Chose the function based on the functions imperative verb\n"
#             " - 2.: If you cannot find the right function for the activity return an error message.\n\n")

# def add_knowledge():
#     return  " Function calling is a powerful feature that significantly enhances the" \
#             " capabilities of Large Language Models (LLMs). It enables better functionality," \
#             " immediate data access and interaction, and sets up for integration with" \
#             " external APIs and services. Function calling turns LLMs into adaptable" \
#             " tools for various use case scenarios." \
#             " Function calling enhances the capabilities of LLMs beyond just text" \
#             " generation. It allows to convert human-generated prompts into precise function" \
#             " invocation descriptors. These descriptors can then be used by connected LLM frameworks" \
#             " to perform computations, manipulate data, and interact with external APIs."\
#             " This expansion of functionality makes LLMs adaptable tools for a wide array"\
#             " of tasks and industries. \n\n"

def add_output_pattern():
     return (" +++ TEMPLATE PATTERN +++\n" 
             " Use the provided template below to return the output: \n"
             " {\"function\": \"function_name\"} \n"
             " - function_name: place holder for the chosen name of the function from the repository."
             " Always inlcude an imperative verb, what the activity can do\n"
             " +++ ERROR HANDLING +++\n"
             " - If you were unsuccessfull chosing a function for the activity, return: Selection error \n")

def add_function_repository(function_repository:list[dict]):
    text = ("These are all functions from the function repository: \n"
            "++++++++++Start Function Repository++++++++++\n")
    
    for i, function in enumerate(function_repository):
        text += f"Function {i+1} --> {function} \n"

    text += "++++++++++End Function Repository++++++++++\n\n"
    return text




def get_sys_message(function_repository:list[dict]):
    sys_message = add_role()
    sys_message += add_knowledge()
    sys_message += add_least_to_most()
    sys_message += add_function_repository(function_repository)
    sys_message += add_output_pattern()
    return sys_message

def get_prompt(activity:str, workflow:str):
    prompt =    f" Chose for the given activity the right function to execute.\n" \
                f" - Activity is: {activity} \n\n"\
                f" - Workflow description is: {workflow} \n\n"
                
    return prompt