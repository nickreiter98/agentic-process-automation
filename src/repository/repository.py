import inspect
import src.repository.interfaces as intf
from src.utils.json_representation import convert_function_to_json_representation


from typing import Any, Dict, List, Union, Literal, Callable

class Repository:
    def __init__(self):
        self.interfaces:List[Callable] = self._get_all_interfaces()
        assert self.interfaces is not None

    def _get_all_interfaces(self) -> List[Callable]:
        functions = []    
        for name, obj in inspect.getmembers(intf):
            if inspect.isfunction(obj) and name.startswith('d_'):
                functions.append(obj)
        return functions
    
    def map_name_to_interface(self) -> Dict[str,Callable]:
        return {i.__name__: i for i in self.interfaces}
    
    def retrieve_interface(self, name:str) -> Callable:
        return self.map_name_to_interface().get(name)
    
    def retrieve_json_representation_by_name(self, name:str) -> Dict[str,Any]:
        return convert_function_to_json_representation(self.retrieve_interface(name))
    
    def retrieve_json_representations(self) -> List[Dict[str,Any]]:
        return [convert_function_to_json_representation(i) for i in self.interfaces]

    
