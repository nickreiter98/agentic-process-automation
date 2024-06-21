import os
import sys
import pandas as pd
from xhtml2pdf import pisa 
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.execution.executer import WorkflowExecutor
from src.modelling.workflow_generation import generate_workflow 

def render_pdf(current_time, name, workflow, workflow_str, workflow_image, execution_text, folder_path, iterations):
   env = Environment(loader=FileSystemLoader('.'))
   # Get the rendering template and render it
   template = env.get_template("test/test_template.html")
   rendered_template = template.render(
      current_time=current_time,
      name=name,
      workflow=workflow,
      process_text=workflow_str.replace('\n', '<br>'),
      process_image=workflow_image+'.png',
      execution_text=execution_text.replace('\n', '<br>'),
      iterations=iterations
   )
   pdf = open(f'{folder_path}/{name}.pdf', 'w+b')
   pisa_status = pisa.CreatePDF(rendered_template, dest=pdf)
   pdf.close()
   pisa_status.err

   # Delete the workflow image and gviz file
   try:
      os.remove(workflow_image)
      os.remove(workflow_image + '.png')
   except:
      pass

if __name__ == '__main__':
   current_time = datetime.today().strftime('%Y_%m_%d-%H:%M:%S')
   # If the folder does not exist, create it
   if not os.path.exists(f'test/{current_time}'):
      os.makedirs(f'test/{current_time}')
   folder_path = f'test/{current_time}'

   workflows = pd.read_csv('test/workflow_descriptions.csv', index_col=0)

   # Iterate over the workflows
   for index, row in workflows.iterrows():
      content = row['content']
      workflow_str = ''
      workflow_image = ''
      execution_log = ''
      try:
         # Generate the workflow
         workflow, iterations = generate_workflow(content, 10)
         workflow_str = workflow.__str__()
         worklfow_gviz = workflow.get_bpmn()
         workflow_image = f'{folder_path}/{index}'
         worklfow_gviz.render(workflow_image, format='png')
         try:
            # Execute the workflow
            executer = WorkflowExecutor(content, workflow)
            executer.run()
            execution_log = executer.get_log()
            render_pdf(current_time, index, content, workflow_str, workflow_image, execution_log, folder_path, iterations)
         # If an error occurs during the execution, render the pdf with the error
         except Exception as e:
            error = f'<span style="color: red;">{type(e).__name__}: {str(e)}</span>'
            render_pdf(current_time, index, content, workflow_str, workflow_image, error, folder_path, iterations)
      # If an error occurs during the generation, render the pdf with the error
      except Exception as e:
         error = f'<span style="color: red;">{type(e).__name__}: {str(e)}</span>'
         render_pdf(current_time, index, content, error, workflow_image, execution_log, folder_path, iterations)