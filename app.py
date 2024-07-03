import pickle
import logging
from datetime import date
from colorama import Fore, Back, Style


httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.CRITICAL)

from src.execution.executor import WorkflowExecutor
from src.modelling.workflow_generation import generate_workflow

if __name__ == "__main__":

    while True:
        try:
            print(
                Fore.RED
                + "Enter your Textual Workflow to be modelled and excecuted:"
                + Style.RESET_ALL
            )
            textual_workflow = input(Fore.GREEN + "Workflow: " + Style.RESET_ALL)

            workflow_processor, _ = generate_workflow(textual_workflow, 10)

            print(workflow_processor.__str__())

            executor = WorkflowExecutor(textual_workflow, workflow_processor)
            executor.run()
            print(executor.get_log())
            print(Fore.GREEN + "Execution completed successfully." + Style.RESET_ALL)
        except (Exception, RuntimeError) as e:
            print(e)
            print(Fore.RED + f"Error: {e}. Please try again!." + Style.RESET_ALL)
            continue

