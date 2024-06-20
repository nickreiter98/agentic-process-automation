import os
import sys
import pandas as pd
from xhtml2pdf import pisa 
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.utils.output_redirection import _print
from src.execution.executer import WorkflowExecutor
from src.modelling.workflow_generation import generate_workflow 

def render_pdf(current_time, name, workflow, process_text, process_image, execution_text, folder_path):
   env = Environment(loader=FileSystemLoader('.'))
   template = env.get_template("test/test_template.html")
   rendered_template = template.render(
      current_time=current_time,
      name=name,
      workflow=workflow,
      process_text=process_text.replace('\n', '<br>'),
      process_image=process_image+'.png',
      execution_text=execution_text
   )
   pdf = open(f'{folder_path}/{name}.pdf', 'w+b')
   pisa_status = pisa.CreatePDF(rendered_template, dest=pdf)
   pdf.close()
   pisa_status.err

   try:
      os.remove(process_image)
      os.remove(process_image + '.png')
   except:
      pass

if __name__ == '__main__':
   current_time = datetime.today().strftime('%Y_%m_%d-%H:%M:%S')
   if not os.path.exists(f'test/{current_time}'):
      os.makedirs(f'test/{current_time}')
   folder_path = f'test/{current_time}'

   workflows = pd.read_csv('test/workflow_descriptions.csv', index_col=0)

   for index, row in workflows.iterrows():
      content = row['content']
      process_text = ''
      process_image = ''
      execution_text = ''
      try:
         process = generate_workflow(content, 10)
         process_text = process.__str__()
         process_gviz = process.get_bpmn()
         process_image = f'{folder_path}/{index}'
         process_gviz.render(process_image, format='png')
         try:
            executer = WorkflowExecutor(content, process)
            executer.run()
            execution_text = executer.logs
            render_pdf(current_time, index, content, process_text, process_image, execution_text, folder_path)
         except Exception as e:
            error = f'<span style="color: red;">{type(e).__name__}: {str(e)}</span>'
            render_pdf(current_time, index, content, process_text, process_image, error, folder_path)
      except Exception as e:
         error = f'<span style="color: red;">{type(e).__name__}: {str(e)}</span>'
         render_pdf(current_time, index, content, error, process_image, execution_text, folder_path)