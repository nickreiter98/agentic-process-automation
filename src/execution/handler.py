import os
import json
import re

from src.utils.open_ai import OpenAIConnection
from src.execution import prompt_arguments, prompt_selection
from src.repository.repository import Repository

from openai import OpenAI
from pm4py.objects.bpmn.obj import BPMN

# Define type hints
from typing import Optional, TypeAlias

StartEvent: TypeAlias = BPMN.StartEvent
EndEvent: TypeAlias = BPMN.EndEvent
Task: TypeAlias = BPMN.Task
ExclusiveGateway: TypeAlias = BPMN.ExclusiveGateway
ParallelGateway: TypeAlias = BPMN.ParallelGateway
Node: TypeAlias = BPMN.BPMNNode
Edge: TypeAlias = BPMN.Flow


class FunctionSelector:
    def __init__(self, repository: Repository):
        self.llm_connection = OpenAIConnection()
        self.repository = repository

    def select(self, task: Node) -> str:
        """Selects the interface for a given task.

        :param task: the task for which the interface should be selected
        :raises Exception: No interface can be mapped to the task
        :raises Exception: Multiple interfaces selected
        :raises Exception: Random error
        :return: the selected interface
        """
        DICT_PATTERN = r"{(.*?)}"
        ERROR_PATTERN = r"Selection error"

        # Create the prompt for function selection
        json_representations = self.repository.retrieve_json_representations()
        sys_message = {
            "role": "system",
            "content": prompt_selection.get_sys_message(json_representations)
        }
        prompt = {"role": "user", "content": prompt_selection.get_prompt(task)}
        message = [sys_message, prompt]

        response = self.llm_connection.request(message)

        # Selection lead to error
        if re.search(ERROR_PATTERN, response, re.IGNORECASE):
            raise Exception(
                f"Mapping error - No interface can be mapped "
                f"to the task '{task.name}'"
            )
        # Selection was successful
        elif re.search(DICT_PATTERN, response, re.DOTALL):
            # Extract the interface as str
            match = re.search(DICT_PATTERN, response, re.DOTALL).group()
            # Load the interface as a dictionary
            interface = json.loads(match)
            # Check if only one interface was selected
            if len(interface) == 1:
                raise Exception(
                "Multiple interfaces selected - Only one interface can be selected"
                )
            clear_name = list(interface.values())[0]
            return clear_name
        # Random error
        else:
            raise Exception(
                "Neither an assignation error nor arguments could be detected "
                "within the response. Please try again!"
            )

class ParameterAssignator:
    def __init__(self, repository: Repository):
        self.llm_connection = OpenAIConnection()
        self.repository = repository

    def assign(self, interface: str, textual_workflow: str, output_storage) -> dict:
        """Assigns the parameters for a given interface.

        :param interface: the interface for which the parameters should be assigned
        :param textual_workflow: the textual representation of the workflow
        :param output_storage: the output storage for the workflow
        :raises Exception: No arguments can be assigned to the interface
        :raises Exception: random error
        :return: the assigned arguments
        """
        DICT_PATTERN = r"{(.*?)}"
        ERROR_PATTERN = r"Assignation error"

        # Create the prompt for parameter assignment
        sys_message = {
            "role": "system",
            "content": prompt_arguments.get_sys_message()
        }
        prompt = {
            "role": "user",
            "content": prompt_arguments.get_prompt(
                self.repository.retrieve_json_representation_by_name(interface),
                textual_workflow,
                output_storage,
            )
        }
        message = [sys_message, prompt]

        response = self.llm_connection.request(message)

        # Selection lead to error
        if re.search(ERROR_PATTERN, response, re.IGNORECASE):
            raise Exception(
                f"Assignation error - No parameters can be assigned"
                f"to the interface '{interface}'"
            )
        # Response was successful
        elif re.search(DICT_PATTERN, response, re.DOTALL):
            # Extract the arguments as str
            match = re.search(DICT_PATTERN, response, re.DOTALL).group()
            # Load the arguments as a dictionary
            arguments = json.loads(match)
            return arguments
        # Random error
        else:
            raise Exception(
                "Neither an assignation error nor arguments could be detected "
                "within the response. Please try again!"
            )
