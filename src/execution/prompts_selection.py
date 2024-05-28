def add_role():
    return  ("Your role: you are an expert in function calling," 
             " familiar with common function calling approaches." 
             " Your task is to map a sub-process/activity from a workflow description" 
             " to a function by selecting the function from a function collection" 
             " When selecting the function, be as precise as possible" 
             " and capture all details from the sub-process/activity as well as the"
             " context from the workflow description in the function." 
             " Also act as the process owner and use" 
             " your expertise and familiarity with the" 
             " workflow process context to avoid any irrational selections. \n\n")

def add_knowledge():
    return  ("Function calling is a powerful feature that significantly enhances the" 
             " capabilities of Large Language Models (LLMs). It enables better functionality," 
             " immediate data access and interaction, and sets up for integration with" 
             " external APIs and services. Function calling turns LLMs into adaptable" 
             " tools for various use case scenarios." 
             " Function calling enhances the capabilities of LLMs beyond just text" 
             " generation. It allows to convert human-generated prompts into precise function" 
             " invocation descriptors. These descriptors can then be used by connected LLM frameworks" 
             " to perform computations, manipulate data, and interact with external APIs."
             " This expansion of functionality makes LLMs adaptable tools for a wide array"
             " of tasks and industries. \n\n")

def add_least_to_most():
    return  ("Your Task is: Chose the name of the function that best represents the sub-process/activity" 
             " and return only the name of the function nothing else." 
             " If you are unable to find a suitable function for the activity, return an error message. \n\n")

def add_output_pattern():
     return ("Use the provided template below to return the output:\n"
             " ```json\n{\"function\": \"function_name\"}\n``` \n"
             " - function_name: place holder for the chosen name of the function from the repository.\n"
             " If you were unsuccessfull chosing a function for the activity, return the output:\n"
             " 'Selection Error' \n\n")

def add_function_repository(function_repository:list[dict]):
    text = "These are the function head descriptions from all functions from the function repository: \n"
    for i, function in enumerate(function_repository):
        text += f"Function {i+1}:\n{function}\n"
    text += "\n\n"
    return text

def get_sys_message(function_repository:list[dict]):
    sys_message = add_role()
    sys_message += add_knowledge()
    sys_message += add_least_to_most()
    sys_message += add_function_repository(function_repository)
    sys_message += add_output_pattern()
    return sys_message

def get_prompt(activity:str):
    prompt = ("Chose for the given activity the right function to execute.\n" 
              f" - Activity is: {activity} \n")
                
    return prompt