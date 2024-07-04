from src.modelling.code_extraction import extract_final_python_code
from src.modelling import prompt_workflow
from src.utils.open_ai import OpenAIConnection
from src.utils.errors import ModellingError, PythonCodeExtractionError


def generate_workflow(textual_workflow: str, max_iteration: int = 5) -> str:
    """Generates a WorkflowProcessor object form a textual description of a workflow.
    Uses LLM to code the workflow. If abnormalities are found within the
    WorkflowProcessor object, the coding is repeated up to max_iteration times.

    :param textual_workflow: the textual description of the workflow to be modelled
    :param max_iteration: max retries of iterations, defaults to 5
    :return: WorkflowProcessor object
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
            executable_code = extract_final_python_code(response)
            local_vars = {}
            # Execute the code to create the model
            exec(executable_code, globals(), local_vars)
            print("Model generation successful")
            # Extract the WorkflowProcessor object from the local variables
            workflow_processor = local_vars["model"]
            return (workflow_processor, i+1)
        # breaks the loop and raises error if workflow cannot be modelled
        except ModellingError as error:
            raise ModellingError()
        # continues loop if Python code extraction error occurs or code cannot be executed
        except (PythonCodeExtractionError, Exception) as error:
            error_description = str(error)
            new_message = f"Executing your code led to the error {error_description}"
            print(new_message)
            # Add the error to the message to be sent to the LLM
            messages.append({"role": "user", "content": new_message})
