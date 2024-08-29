from src.modeling.code_extraction import extract_python_code
from src.modeling import prompt_workflow
from src.utils.open_ai import OpenAIConnection
from src.utils.errors import ModellingError, PythonCodeExtractionError


def generate_processor(textual_workflow: str, max_iteration: int = 5) -> str:
    """Generates a ProcessProcessor object form a textual description of a workflow.
    Uses LLM to code the process. If abnormalities are found within the
    ProcessProcessor object, the coding is repeated up to max_iteration times.

    :param textual_workflow: the textual description of the workflow to be modelled
    :param max_iteration: max retries of iterations, defaults to 5
    :return: ProcessProcessor object
    """
    # Create the prompt for the model generation
    prompt = prompt_workflow.create_model_generation_prompt(textual_workflow)
    messages = [{"role": "user", "content": prompt}]

    llm_connection = OpenAIConnection()

    for i in range(max_iteration):
        try:
            print(f"Iteration {i+1} of model generation")
            # Request the LLM to generate the model
            response = llm_connection.request(messages)
            messages.append({"role": "system", "content": response})
            # Extract the executable code from the response
            executable_code = extract_python_code(response)
            local_vars = {}
            # Execute the code to create the model
            exec(executable_code, globals(), local_vars)
            print("Model generation successful")
            # Extract the WorkflowProcessor object from the local variables
            process_processor = local_vars["model"]
            return (process_processor, i+1)
        # breaks the loop and raises error if workflow cannot be modelled
        except ModellingError:
            raise ModellingError("Given textual workflow is not a business/IT process")
        # continues loop if Python code extraction error occurs or code cannot be executed
        except (PythonCodeExtractionError, Exception) as error:
            error_description = str(error)
            new_message = f"Executing your code led to the error {error_description}"
            print(new_message)
            # Add the error to the message to be sent to the LLM
            messages.append({"role": "user", "content": new_message})
