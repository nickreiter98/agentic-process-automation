def add_role():
    return (
        "Your role: imagine you are an exclusive gateway, and you are able "
        "to choose the right condition given data to a specific context \n\n"
    )


def add_least_to_most():
    return (
        "Select the right condition based on the given data. For this "
        "follow the upcoming steps:\n"
        "- 1.: Read the data carefully and understand the context of the "
        "data to compare.\n"
        "- 2.: Compare the data with the conditions and choose the right "
        "condition.\n"
        "- 3.: If you cannot find the right condition, return an error "
        "message.\n"
        "- 4.: If you have found the right condition, return your findings\n\n"
    )


def add_output_pattern():
    return (
        "Use the provided template below to return the output:\n"
        '```json\n{"name": "condition"}\n```'
        "- condition: placeholder for the name of the condition which is "
        "chosen.\n"
        "If you were unsuccessful choosing a function, return the output:\n"
        "'Condition error' \n\n"
    )


def get_sys_message():
    sys_message = add_role()
    sys_message += add_least_to_most()
    sys_message += add_output_pattern()
    return sys_message


def get_prompt(context: str, conditions: list[str], output: str):
    prompt = "Choose one of the following conditions:\n"

    for i, condition in enumerate(conditions):
        prompt += f"```{condition}```\n"

    prompt += (
        "based on the given data and context. \n"
        f"- Data: {output} \n"
        f"- Context: {context} \n"
    )

    return prompt
