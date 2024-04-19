def add_role():
    return  " Your role: you are an expert in function calling," \
            " familiar with common function calling approaches." \
            " Your task is to map a sub-process from a workflow description" \
            " to a function by selecting the function from a function collection" \
            " When selecting the function, be as precise as possible" \
            " and capture all details from the sub-process as well as the"\
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

def add_exact_task():
    return  " Your Task is: Chose the name of the function that best represents the sub-process" \
            " and return only the name of the function nothing else. \n\n"

def add_function_repository(function_repository:list[dict]):
    return  f" This is the function repository: \n" \
            f" {function_repository} "


def get_sys_message(function_repository:list[dict]):
    sys_message = add_role()
    sys_message += add_knowledge()
    sys_message += add_exact_task()
    sys_message += add_function_repository(function_repository)
    return sys_message

def get_prompt(sub_process:str, worklfow:str):
    prompt =    f" Chose for the given sub-process the right function to execute." \
                f" The sub-process is: {sub_process} "\
                f" The workflow description is: {worklfow} \n\n"
    return prompt