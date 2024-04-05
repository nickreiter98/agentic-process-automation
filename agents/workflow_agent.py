from openai import OpenAI
from misc.directed_graph import DirectedGraph
from agents.function_calling_agent import Agent as FuncAgent
from agents.function_calling_agent import FunctionSelector, ParameterAssignator
from misc import decoder

from func_repository.repository import Repository

import os
import json
import logging

sys_message = '''You are modeling a process workflow. You are given a textual description of a process workflow. 
The aim is to return the workflow description as a directional graph.
Every described function from the text is mapped to a node. Keep the context of the function and include rather more information for one task.
The graph must be returned in a JSON representation. The key is the source node and the values are the target nodes stored in a list.
I give some examples.

Example 1:
I would like to know how warm it is in Berlin. Put the information in an email. Afterwards send the to nick.reiter@hotmail.de  and store the email on the disk.
{
    "get the weather data of Berlin": ["write the email"],
    "write the email": ["send the email to nick.reiter@hotmail.de", "store the email on the disk"],
    "send the email to nick.reiter@hotmail.de": [],
    "store the email on the disk": []

}

Example 2:
Get the bank account statement of user max.mustermann. If the bank account statement is higher than 1000€, get the users email address and send him the current bank account statement via email. if the bank account statement is lower than 1000€, abort the process.
{
    "get bank account statement of user max.mustermann": ["bank account statement is higher than 1000€, get users email address. If lower than 1000€, abort the process"],
    "bank account statement is higher than 1000€, get users email address. If lower than 1000€, abort the process": ["get users email address", "abort the process"],
    "get users email address": ["send the current bank account statement via email to the user"],
    "abort the process: [],
    "send the current bank account statement via email to the user": []

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
        self.mapping = None

    def run (self, query:str):
        self.query = query
        self.chat_history.append({'role': 'user', 'content': query})
        res = self.client.chat.completions.create(
                model=self.model,
                messages=self.chat_history
            )
        self.response = res.choices[0].message.content
        self.chat_history.append({'role': 'assistant', 'content': self.response})

    def map_functions_to_str_representation(self):
        try:
            workflow = json.loads(self.response)
        except:
            print('Could not parse the response to a JSON object')
        else:
            fagent = FuncAgent(functions=self.functions)

            output=''
            self.mapping = {}
            str_representations = []
            for task in workflow:
                temp = fagent.get_function(task, output)
                str_representations.append(temp)
                self.mapping[task] = temp

        return str_representations
        
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


    def show_directed_graph(self, mode:list['normal', 'mapping'] = 'normal'):
        graph = DirectedGraph()

        workflow = json.loads(self.response)

        if mode == 'normal':
            for key in workflow:
                values = workflow[key]
                for value in values:
                    graph.add_edge(key, value)

        elif mode == 'mapping':
            for key in workflow:
                values = workflow[key]
                if not values:
                    pass
                else:
                    for value in values:
                        graph.add_edge(self.mapping[key], self.mapping[value])

        graph.display()

    def get_functions(self):
        fagent = FuncAgent(functions=self.functions)
        return fagent.functions
    
class WorkflowExecutor():
    def __init__(
        self,
        workflow_description: str,
        workflow_representation: str,
    ):
        self.functions = self._get_function_repository()
        self.workflow_description = workflow_description
        self.workflow_representation = json.loads(workflow_representation)
        self.workflow_functions = {}
        self.func_mapping = self._create_func_mapping(self.functions)

    def _get_function_repository(self):
        return Repository().functions
    
    def _create_func_mapping(self, functions: list) -> dict:
        if functions is None:
            return {}
        return {func.__name__: func for func in functions}
    
    def map_to_functions(self):
        selector = FunctionSelector(functions=self.functions)

        mapping = {}

        for sub_process in self.workflow_representation:
            mapping[sub_process] = selector.select(sub_process, self.workflow_description)

        #self.workflow_functions = self.workflow_representation.copy()

        successor = None
        for sub_process in self.workflow_representation:
            successor = self.workflow_representation[sub_process]
            if not successor:
                self.workflow_functions[mapping[sub_process]] = 'None'
            elif len(successor) == 1:
                self.workflow_functions[mapping[sub_process]] = mapping[successor[0]]
            elif len(successor) > 1:
                for succ in successor:
                    self.workflow_functions[mapping[sub_process]] = mapping[succ]


        return self.workflow_functions
    
    def execute(self):
        assignator = ParameterAssignator(functions=self.functions)

        output = ''
        for fnct in self.workflow_functions:
            args = assignator.assign(fnct, output, self.workflow_description)
            args = json.loads(args)
            output = self.func_mapping[fnct](**args)
       

            