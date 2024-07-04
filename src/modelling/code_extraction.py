import re

from src.utils.errors import ModellingError, PythonCodeExtractionError

def extract_final_python_code(response_text:str) -> str:
    """Extracts the final Python code snippet from the response text from LLM
    and returns an executable Python code snippet.
    Also checks whether the import statement is correct.

    :param response_text: the response text from the LLM
    :raises Exception: if the Python code snippet does not meet the import statement requirements
    :raises Exception: if no Python code snippet is found
    :return: executable Python code snippet
    """
    # Define the pattern for the Python code snippet
    python_code_pattern = r"```python(.*?)```"
    allowed_import_path = "src.modelling.workflow_processor"
    allowed_import_class = "WorkflowProcessor"
    any_import_pattern = r"^\s*(from\s+\S+\s+import\s+\S+|import\s+\S+)"
    allowed_import_pattern = (
        r"^\s*(from\s+"
        + re.escape(allowed_import_path)
        + r"\s+import\s+"
        + re.escape(allowed_import_class)
        + r"|import\s+"
        + re.escape(allowed_import_path)
        + r"\."
        + re.escape(allowed_import_class)
        + r")\s*$"
    )
    ERROR_PATTERN = r"Modelling Error"

    if re.search(ERROR_PATTERN, response_text, re.IGNORECASE):
        raise ModellingError()
    else:
        pass

    # Find Python code snippet in the response text
    matches = re.findall(python_code_pattern, response_text, re.DOTALL)

    # Check if python code snippet is found
    if matches: 
        # Remove leading and trailing whitespaces 
        python_snippet = matches[-1].strip()
        # Split the Python code snippet into lines
        lines = python_snippet.split('\n')
        for line in lines:
            # Check if the import statement is comprised in the Python code snippet
            if re.match(any_import_pattern, line):
                if not re.match(allowed_import_pattern, line):
                    raise PythonCodeExtractionError(
                        f"Python snippet does not meet the import statement "
                        f"requirements! Only the following import"
                        f"statement is allowed:\n"
                        f"from {allowed_import_path} import {allowed_import_class}"
                    )
        return python_snippet
    # No Python code snippet found
    else:
        raise PythonCodeExtractionError("No Python code snippet found!")