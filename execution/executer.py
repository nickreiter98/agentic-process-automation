from openai import OpenAI
from misc.directed_graph import DirectedGraph
from execution.handler import FunctionSelector, ParameterAssignator
from misc import decoder

from repository.repository import Repository

import os
import json
import logging

    
class Executor():
    def __init__(
        self,
        workflow_description: str,
        workflow_representation: str,
    ):
        self.functions = self._get_function_repository()
        self.workflow_description = workflow_description
        self.workflow_representation = workflow_representation
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
            if sub_process == 'Start':
                pass
            else:
                mapping[sub_process] = selector.select(sub_process, self.workflow_description)

        #self.workflow_functions = self.workflow_representation.copy()

        for sub_process in self.workflow_representation:
            if sub_process == 'Start':
                pass
            else:
                successor = self.workflow_representation[sub_process]
                if len(successor) == 1:
                    if successor[0][0] == 'End':
                        self.workflow_functions[mapping[sub_process]] = 'End'
                    else:
                        self.workflow_functions[mapping[sub_process]] = mapping[successor[0][0]]
                elif len(successor) > 1:
                    for succ in successor:
                        if succ[0][0] == 'End':
                            self.workflow_functions[mapping[sub_process]] = 'End'
                        else:
                            self.workflow_functions[mapping[sub_process]] = mapping[succ[0][0]]


        return self.workflow_functions
    
    def execute(self):
        assignator = ParameterAssignator(functions=self.functions)

        output = ''
        for fnct in self.workflow_functions:
            args = assignator.assign(fnct, output, self.workflow_description)
            args = json.loads(args)
            output = self.func_mapping[fnct](**args)
       

            