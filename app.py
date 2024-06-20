import pickle
import logging
from datetime import date
from colorama import Fore, Back, Style


httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.CRITICAL)

from src.execution.executer import WorkflowExecutor
from src.modelling.workflow_generation import generate_workflow

if __name__ == '__main__':

   while True:
      try:
         print(Fore.RED + 'Enter your Textual Workflow to be modelled and excecuted:' + Style.RESET_ALL)
         workflow = input(Fore.GREEN + 'Workflow: ' + Style.RESET_ALL)

         process = generate_workflow(workflow, 10)
         
         print(process.__str__())

         executer = WorkflowExecutor(workflow, process)
         executer.run()
         print(executer.get_log())
         print(Fore.GREEN + 'Execution completed successfully.' + Style.RESET_ALL)
      except Exception as e:
         print(e)
         print(Fore.RED + 'An error occured. Please try again.' + Style.RESET_ALL)
         continue

