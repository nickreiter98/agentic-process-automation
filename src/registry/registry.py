import inspect
import src.registry.connectors as connectors
from src.utils.json_representation import convert_function_to_json_representation


from typing import Any, Dict, List, Callable


class Registry:
    def __init__(self):
        self.connectors: List[Callable] = self._get_all_connectors()
        assert self.connectors is not None

    def _get_all_connectors(self) -> List[Callable]:
        """retrieve all connectors from the connectors module

        :return: list of iterface functions
        """
        functions = []
        for name, obj in inspect.getmembers(connectors):
            if (
                inspect.isfunction(obj)
                and obj.__module__ == connectors.__name__
                and not name.startswith("_")
            ):
                functions.append(obj)
        return functions

    def map_name_to_connector(self) -> Dict[str, Callable]:
        """Map the name of the function to the function itself

        :return: dict - name(key) to function(value) mapping
        """
        return {i.__name__: i for i in self.connectors}

    def retrieve_connector(self, name: str) -> Callable:
        """Retrieve the connector by name

        :param name: name of the connector
        :return: function corresponding to the name
        """
        return self.map_name_to_connector().get(name)

    def retrieve_json_representation_by_name(self, name: str) -> Dict[str, Any]:
        """Retrieve the json representation of the connector by name

        :param name: name of the connector
        :return: json representation of the connector
        """
        connector = self.retrieve_connector(name)
        return convert_function_to_json_representation(connector)

    def retrieve_json_representations(self) -> List[Dict[str, Any]]:
        """Retrieve the json representation of all connectors

        :return: list of json representations of the connectors
        """
        return [convert_function_to_json_representation(i) for i in self.connectors]
