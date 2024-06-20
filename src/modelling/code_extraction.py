import re

def extract_final_python_code(response_text:str) -> str:
    python_code_pattern = r"```python(.*?)```"
    allowed_import_path = "src.modelling.generator"
    allowed_import_class = "WorkflowProcessor"
    any_import_pattern = r"^\s*(from\s+\S+\s+import\s+\S+|import\s+\S+)"
    allowed_import_pattern = r"^\s*(from\s+" + re.escape(allowed_import_path) + r"\s+import\s+" + re.escape(
        allowed_import_class) + r"|import\s+" + re.escape(allowed_import_path) + r"\." + re.escape(
        allowed_import_class) + r")\s*$"

    matches = re.findall(python_code_pattern, response_text, re.DOTALL)

    if matches:
        python_snippet = matches[-1].strip()
        lines = python_snippet.split('\n')

        for line in lines:
            if re.match(any_import_pattern, line):
                if not re.match(allowed_import_pattern, line):
                    raise Exception(
                        "Python snippet does not meet the import statement requirements! Only the following import"
                        " statement is allowed: " + 'from ' + allowed_import_path + ' import ' + allowed_import_class)
        return python_snippet

    else:
        raise Exception("No Python code snippet found!")