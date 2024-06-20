import pickle
import logging
from datetime import date
from colorama import Fore, Back, Style

from src.utils.output_redirection import _print

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.CRITICAL)

from src.execution.executer import WorkflowExecutor
from src.modelling.model_generation import generate_model

if __name__ == '__main__':
   
   # logging.basicConfig(filename='build/log.log',
   #                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
   #                   datefmt='%H:%M:%S',
   #                   level=logging.INFO)
   # logger = logging.getLogger("httpx")
   # logger.setLevel(logging.CRITICAL)
   # logger = logging.getLogger(__name__)

   while True:
      try:
         print(Fore.RED + 'Enter your Textual Workflow to be modelled and excecuted:' + Style.RESET_ALL)
         workflow = input(Fore.GREEN + 'Workflow: ' + Style.RESET_ALL)

         process = generate_model(workflow, 10)
         
         print(process.__str__())

         executer = WorkflowExecutor(workflow, process)
         executer.run()
         print(executer.get_log())
         print(Fore.GREEN + 'Execution completed successfully.' + Style.RESET_ALL)
      except Exception as e:
         print(e)
         print(Fore.RED + 'An error occured. Please try again.' + Style.RESET_ALL)
         continue

