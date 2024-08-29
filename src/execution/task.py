import os
import json
import re

from src.utils.open_ai import OpenAIConnection
from src.execution import prompt_arguments, prompt_selection
from src.registry.registry import Registry
from src.utils.errors import FunctionSelectorError, ParameterAssignatorError

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
    def __init__(self, registry: Registry):
        self.llm_connection = OpenAIConnection()
        self.registry = registry

    def select(self, task: Node) -> str:
        """Selects the connector for a given task.

        :param task: the task for which the connector should be selected
        :raises Exception: No connector can be mapped to the task
        :raises Exception: Multiple connectors selected
        :raises Exception: Random error
        :return: the selected connector
        """
        DICT_PATTERN = r"{(.*?)}"
        ERROR_PATTERN = r"Selection error"

        # Create the prompt for function selection
        json_representations = self.registry.retrieve_json_representations()
        sys_message = {
            "role": "system",
            "content": prompt_selection.get_sys_message(json_representations)
        }
        prompt = {"role": "user", "content": prompt_selection.get_prompt(task)}
        message = [sys_message, prompt]

        response = self.llm_connection.request(message)

        # Selection lead to error
        if re.search(ERROR_PATTERN, response, re.IGNORECASE):
            raise FunctionSelectorError(
                f"No connector can be mapped to the task '{task.name}'"
            )
        # Selection was successful
        elif re.search(DICT_PATTERN, response, re.DOTALL):
            # Extract the connector as str
            match = re.search(DICT_PATTERN, response, re.DOTALL).group()
            # Load the connector as a dictionary
            connector = json.loads(match)
            # Check if only one connector was selected
            if len(connector) != 1:
                raise FunctionSelectorError(
                f"Multiple connectors selected for '{task.name}'"
                )
            clear_name = list(connector.values())[0]
            return clear_name
        # Random error
        else:
            raise FunctionSelectorError(f"Unkown error for '{task.name}'")

class ParameterAssignator:
    def __init__(self, registry: Registry):
        self.llm_connection = OpenAIConnection()
        self.registry = registry

    def assign(self, connector: str, textual_workflow: str, data_cache) -> dict:
        """Assigns the parameters for a given connector.

        :param connector: the connector for which the parameters should be assigned
        :param textual_workflow: the textual representation of the workflow
        :param data_cache: the output storage for the workflow
        :raises Exception: No arguments can be assigned to the connector
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
                self.registry.retrieve_json_representation_by_name(connector),
                textual_workflow,
                data_cache,
            )
        }
        message = [sys_message, prompt]

        response = self.llm_connection.request(message)

        # Selection lead to error
        if re.search(ERROR_PATTERN, response, re.IGNORECASE):
            raise ParameterAssignator(
                f"No parameters can be assigned to the connector '{connector}'"
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
            raise ParameterAssignatorError(f"Unkown error for '{connector}'")
