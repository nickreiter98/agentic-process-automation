from openai import OpenAI
from misc.directed_graph import DirectedGraph
from func_agent.agent import Agent as FuncAgent
from misc import decoder

import os
import json
import logging

sys_message = '''You are modeling a process workflow. You are given a textual description of a process workflow. 
The aim is to return the workflow description as a directional graph.
Every described function from the text is mapped to a node. Keep the context of the function and include rather more information for one task.
The graph must be returned in a JSON representation. The key is the source node and the values are the target nodes stored in a list.
I give you an example.
I would like to know how warm it is in Berlin. Put the information in an email. Afterwards send the to nick.reiter@hotmail.de  and store the email on the disk.
{
    "get the weather data of Berlin": ["write the email"],
    "write the email": ["send the email to nick.reiter@hotmail.de", "store the email on the disk"],
    "send the email to nick.reiter@hotmail.de": [],
    "store the email on the disk": []

}
Only provide the clear JSON
If the request is not a textual process worklfow description, behave like a normal chatbot!
'''

class Agent():
    def __init__(
        self,
        model: str = 'gpt-3.5-turbo',
        functions: list = None
    ):
        self.model = model
        self.functions = functions
        self.chat_history = [{'role': 'system', 'content': sys_message}]
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.response = None
        self.query = None

    def converse(self, query:str):
        self.query = query
        self.chat_history.append({'role': 'user', 'content': query})
        res = self.client.chat.completions.create(
                model=self.model,
                messages=self.chat_history
            )
        self.response = res.choices[0].message.content
        self.chat_history.append({'role': 'assistant', 'content': self.response})
        
    # TODO: combine the execute and converse method
    def execute(self):
        try:
            workflow = json.loads(self.response)
        except:
            self.chat_history = [{'role': 'assistant', 'content': self.response}]
            return self.response
        else:
            fagent = FuncAgent(functions=self.functions)

            output=''
            for task in workflow:
                output = fagent.execute_function_call(task, output)


    def show_directed_graph(self):
        dgraph = DirectedGraph()

        res_json = json.loads(self.response)

        for key in res_json:
            values = res_json[key]
            for value in values:
                dgraph.add_edge(key, value)

        dgraph.display()