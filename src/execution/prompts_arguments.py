def add_role():
    return (
        "You are an expert in function calling, familiar with common function "
        "calling approaches. Your task is to assign the parameters of a function "
        "with the right arguments. The arguments can be derived from the output of "
        "the previous function and/or from a workflow description. Note, Previously "
        "activities from the workflow have been mapped to a function. Also act as "
        "the process owner and use your expertise and familiarity with the workflow "
        "process context to avoid any irrational assignments.\n\n"
    )


def add_knowledge():
    return (
        "A parameter assignator refers to a mechanism or a process within a "
        "program that assigns parameters of a function with arguments. A parameter "
        "assignator contains following characteristics:\n"
        " - Argument Extraction: The process of identifying and extracting arguments "
        "or parameters passed to a specific function. Also recognizes if parameters "
        "are optional/required\n"
        " - Type and Value Validation: The process of checking that arguments "
        "provided match the expected types as declared within the function "
        "description. Performing type coercion if needed.\n\n"
    )


def add_least_to_most():
    return (
        "Assign the parameters of the function with arguments. I will provide a "
        "step-by-step schedule:\n"
        " - 1.: Assign all or only the required parameters of the functions with "
        "the help of the output of the previous functions. Decide utilizing your "
        "knowledge which parameters are assigned. Try to assign the parameters by "
        "using the most current output. If this is not possible, jump to the next "
        "output.\n"
        " - 2.: Assign the parameters which haven't been assigned yet with arguments "
        "extracted from the workflow description.\n"
        " - 3.: If assignation is not possible for the required parameters, throw an "
        "Assignation error\n"
        " In the cases decide whether optional arguments are needed or not. If you "
        "cannot assign the parameters, return an error message.\n\n"
    )


def add_errors():
    return (
        "Try to avoid the following errors:\n"
        "- OUTPUT:\n"
        "{'location': {'name': 'Berlin', 'region': 'Berlin', 'country': 'Germany', "
        "'lat': 52.52, 'lon': 13.4,}\n"
        "- WORKFLOW: Get a random location and then write a text about the location.\n\n"
        "- FUNCTION: d_write_text\n"
        "- INPUT: {'text_context': 'Berlin, the capital city of Germany, is a vibrant "
        "metropolis renowned for its cultural diversity, rich history, and dynamic art "
        "scene. This city is not just the political center of Germany but also a pivotal "
        "cultural hub in Europe, blending historical landmarks with modern, cutting-edge "
        "culture.', 'context_info': 'Informal, general information'}\n\n"
        "- ERROR: The output is a dict, but the argument of text_context has already "
        "been formulated. In this case, you are only providing the output for the "
        "function to be called.\n"
        "A possible solution might be: {'text_content': 'Berlin is in Germany and in "
        "the region of Berlin. It is located at lat 52.53 and lon 13.4', "
        "'context_info': 'Informal, general information'}\n"
    )


def add_output_pattern():
    return (
        " Only provide the output in the output pattern. Don't return any "
        "explanation or reasoning. Use the provided template below to return the "
        "output:\n"
        ' ```json\n{"parameter": "value", "parameter": "value"}\n```\n'
        " - parameter: place holder for the name of the parameter to be assigned.\n"
        " - value: place holder for the value to be assigned to the parameter.\n"
        ' Never return ```json\n{"parameter": "value"}\n```\n'
        " If you were unsuccessful assigning required parameters, return the output:"
        " 'Assignation error'\n"
    )


def add_output_storage(output_storage: list[dict[dict]]) -> str:
    if not output_storage:
        return "No output has been stored yet.\n"
    else:
        text = "The output of the previous functions are:\n"
        for i, output in enumerate(output_storage[::-1]):
            assert output is not None
            function_name = list(output.keys())[0]
            function_output = output[function_name]
            text += (
                f"Function {i+1} step ago:\n"
                f"{function_name} with the output --> {function_output}\n"
            )
        return text


def get_sys_message():
    sys_message = add_role()
    sys_message += add_knowledge()
    sys_message += add_least_to_most()
    # sys_message += add_errors()
    sys_message += add_output_pattern()
    return sys_message


from typing import List


def get_prompt(function: dict, workflow: str, output_storage: List[str]):
    prompt = (
        f"Assign the parameter of provided function with arguments.\n"
        f"- Head of the function arguments has to be assigned: {str(function)}\n"
        f"- {add_output_storage(output_storage)}"
        f"- Workflow description: {workflow}\n\n"
    )
    return prompt
