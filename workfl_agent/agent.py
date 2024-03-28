from openai import OpenAI
from graph.directed_graph import DirectedGraph
from func_agent.agent import Agent as FuncAgent
from misc import decoder

import os
import json
import logging

sys_message = '''You are modeling a process workflow. You are given a textual description of a process workflow. 
The aim is to return the workflow description as a directional graph.
Every described function from the text is mapped to a node. Keep the context of the function and include rather more information for one task.
Very important: you can only map a task to a prevalent function from the prevalent list:
The graph must be returned in a JSON representation. The key is the source node and the values are the target nodes stored in a list.
I give you an example.
{}
I would like to know how warm it is in Berlin. Put the information in an email and send it to Nick Reiter.
{{
    'weather in Berlin': ['write an email']
    'write an email': ['send the email']
}}
Only provide the JSON
If the request is not a textual process worklfow description, behave like a normal chatbot!
'''

class Agent():
    def __init__(
        self,
        model: str = 'gpt-4-0613',
        functions: list = None
    ):
        self.model = model
        self.functions = functions
        self.str_func = ''' '''
        for function in functions:
            text = 'START FUNCTION \n {} \n END FUNCTION \n '
            self.str_func += text.format(str(decoder.func_to_json(function)))
        self.chat_history = [{'role': 'system', 'content': sys_message.format(self.str_func)}]
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.last_response = None
        self.last_query = None

    def ask(self, query:str) -> str:
        self.last_query = query
        self.chat_history.append({'role': 'user', 'content': query})
        res = self.client.chat.completions.create(
                model=self.model,
                messages=self.chat_history
            )
        self.last_response = res.choices[0].message.content    

    def execute(self):
        try:
            workflow = json.loads(self.last_response)
        except:
            logging.info('Normal chatbot behavior')
            self.chat_history = [{'role': 'assistant', 'content': self.last_response}]
            return self.last_response
        else:
            logging.info('Executing workflow:')
            fagent = FuncAgent(functions=self.functions)

            output=''
            for task in workflow:
                output = fagent.ask(self.last_query, task, output)

    
    def show_directed_graph(self):
        dgraph = DirectedGraph()

        res_json = json.loads(self.last_response)

        for key in res_json:
            values = res_json[key]
            for value in values:
                dgraph.add_edge(key, value)

        dgraph.display()