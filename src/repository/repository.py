import inspect
import src.repository.interfaces as interfaces
from src.utils.json_representation import convert_function_to_json_representation


from typing import Any, Dict, List, Callable


class Repository:
    def __init__(self):
        self.interfaces: List[Callable] = self._get_all_interfaces()
        assert self.interfaces is not None

    def _get_all_interfaces(self) -> List[Callable]:
        """retrieve all interfaces from the interfaces module

        :return: list of iterface functions
        """
        functions = []
        for name, obj in inspect.getmembers(interfaces):
            if (
                inspect.isfunction(obj)
                and obj.__module__ == interfaces.__name__
                and not name.startswith("_")
            ):
                functions.append(obj)
        return functions

    def map_name_to_interface(self) -> Dict[str, Callable]:
        """Map the name of the function to the function itself

        :return: dict - name(key) to function(value) mapping
        """
        return {i.__name__: i for i in self.interfaces}

    def retrieve_interface(self, name: str) -> Callable:
        """Retrieve the interface by name

        :param name: name of the interface
        :return: function corresponding to the name
        """
        return self.map_name_to_interface().get(name)

    def retrieve_json_representation_by_name(self, name: str) -> Dict[str, Any]:
        """Retrieve the json representation of the interface by name

        :param name: name of the interface
        :return: json representation of the interface
        """
        interface = self.retrieve_interface(name)
        return convert_function_to_json_representation(interface)

    def retrieve_json_representations(self) -> List[Dict[str, Any]]:
        """Retrieve the json representation of all interfaces

        :return: list of json representations of the interfaces
        """
        return [convert_function_to_json_representation(i) for i in self.interfaces]
