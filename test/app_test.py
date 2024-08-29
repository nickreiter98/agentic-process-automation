import os
import sys
import pandas as pd
from xhtml2pdf import pisa 
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.execution.execution import ProcessExecutor
from src.modeling.generate_processor import generate_processor
def render_pdf(current_time, name, workflow, workflow_str, process_image, execution_text, folder_path, iterations):
   env = Environment(loader=FileSystemLoader('.'))
   # Get the rendering template and render it
   template = env.get_template("test/test_template.html")
   rendered_template = template.render(
      current_time=current_time,
      name=name,
      workflow=workflow,
      process_text=workflow_str.replace('\n', '<br>'),
      process_image=process_image+'.png',
      execution_text=execution_text.replace('\n', '<br>'),
      iterations=iterations
   )
   pdf = open(f'{folder_path}/{name}.pdf', 'w+b')
   pisa_status = pisa.CreatePDF(rendered_template, dest=pdf)
   pdf.close()
   pisa_status.err

   # Delete the workflow image and gviz file
   try:
      os.remove(process_image)
      os.remove(process_image + '.png')
   except:
      pass

if __name__ == '__main__':
   current_time = datetime.today().strftime('%Y_%m_%d-%H:%M:%S')
   # If the folder does not exist, create it
   glob_folder_path = f'test/{current_time}'
   if not os.path.exists(glob_folder_path):
      os.makedirs(glob_folder_path)

   names = ["normal", "bullet_points", "difficult_context"]
   workflows = []
   for name in names:
      workflows.append(pd.read_csv(f'test/workflow_descriptions_{name}.csv', index_col=0))

   # Iterate over the workflows
   for i, workflow in enumerate(workflows):
      folder_path = f'{glob_folder_path}/{names[i]}'
      if not os.path.exists(folder_path):
         os.makedirs(folder_path)
      for index, row in workflow.iterrows():
         content = row['content']
         process_str = ''
         process_image = ''
         execution_log = ''
         try:
            # Generate the process processor
            process_processor, iterations = generate_processor(content, 10)
            process_str = process_processor.__str__()
            process_gviz = process_processor.get_bpmn()
            process_image = f'{folder_path}/{index}'
            process_gviz.render(process_image, format='png')
            try:
               # Execute the process
               executor = ProcessExecutor(content, process_processor)
               executor.run()
               execution_log = executor.get_log()
               render_pdf(current_time, index, content, process_str, process_image, execution_log, folder_path, iterations)
            # If an error occurs during the execution, render the pdf with the error
            except Exception as e:
               error = f'<span style="color: red;">{str(e)}</span>'
               render_pdf(current_time, index, content, process_str, process_image, error, folder_path, iterations)
         # If an error occurs during the generation, render the pdf with the error
         except Exception as e:
            error = f'<span style="color: red;">{str(e)}</span>'
            render_pdf(current_time, index, content, error, process_image, execution_log, folder_path, None)
         print("++++++++++++++++++")