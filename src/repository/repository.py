import inspect
import src.repository.interfaces as intf

import functools
import inspect
import re

from typing import Any, Dict, List, Union, Literal, Callable

class Repository:
    def __init__(self):
        self.functions:List[Callable] = self._get_functions()

    def _get_functions(self) -> List[Callable]:
        functions = []    
        for name, obj in inspect.getmembers(intf):
            if inspect.isfunction(obj) and name.startswith('d_'):
                functions.append(obj)
        return functions
    
    def get_functions(self) -> List[Callable]:
        return self.functions
    
    def get_name_to_function(self) -> Dict[str,Callable]:
        assert self.functions is not None
        return {func.__name__: func for func in self.functions}
    
    def get_function_by_name(self, name:str) -> Callable:
        assert self.functions is not None
        return self.get_name_to_function().get(name)
    
    def get_json_by_name(self, name:str) -> Dict[str,Any]:
        assert self.functions is not None
        return self._function_to_json(self.get_function_by_name(name))
    
    def get_function_to_json(self) -> List[Dict[str,Any]]:
        return [self._function_to_json(func) for func in self.functions]

    def _function_to_json(self, func, format:str = 'normal'):
        # Check if the function is a functools.partial
        if isinstance(func, functools.partial) or isinstance(func, functools.partialmethod):
            fixed_args = func.keywords
            _func = func.func
            if isinstance(func, functools.partial) and (fixed_args is None or fixed_args == {}):
                fixed_args = dict(zip(func.func.__code__.co_varnames, func.args))
        else:
            fixed_args = {}
            _func = func

        # first we get function name
        func_name = _func.__name__
        # then we get the function annotations
        argspec = inspect.getfullargspec(_func)
        # get the function docstring
        func_doc = inspect.getdoc(_func)
        # parse the docstring to get the description
        func_description = ''.join([line for line in func_doc.split("\n") if not line.strip().startswith(':')])
        # parse the docstring to get the descriptions for each parameter in dict format
        param_details = self._extract_params(func_doc) if func_doc else {}
        # attach parameter types to params and exclude fixed args
        # get params
        params = {}
        for param_name in argspec.args:
            if param_name not in fixed_args.keys():
                params[param_name] = {
                    "description": param_details.get(param_name) or "",
                    "type": self._type_mapping(argspec.annotations.get(param_name, type(None)))
                }
        # calculate required parameters excluding fixed args
        # _required = [arg for arg in argspec.args if arg not in fixed_args]
        _required = [i for i in argspec.args if i not in fixed_args.keys()]
        sig = inspect.signature(_func)
        requ_params = sig.parameters
        _required = [name for name, param in requ_params.items() if param.default == inspect.Parameter.empty]
        # if inspect.getfullargspec(_func).defaults:
        #     _required = [argspec.args[i] for i, a in enumerate(argspec.args) if
        #                 argspec.args[i] not in inspect.getfullargspec(_func).defaults and argspec.args[
        #                     i] not in fixed_args.keys()]
        # then return everything in dict

        if format == 'normal':
            return {
                "name": func_name,
                "description": func_description,
                "parameters": {
                    "type": "object",
                    "properties": params
                },
                "required": _required
            }
        elif format == 'arguments':
            return {
                "parameters": params,
                "required": _required
            }
        
    def _extract_params(self, doc_str: str):
        # split doc string by newline, skipping empty lines
        params_str = [line for line in doc_str.split("\n") if line.strip()]
        params = {}
        for line in params_str:
            # we only look at lines starting with ':param'
            if line.strip().startswith(':param'):
                param_match = re.findall(r'(?<=:param )\w+', line)
                if param_match:
                    param_name = param_match[0]
                    desc_match = line.replace(f":param {param_name}:", "").strip()
                    # if there is a description, store it
                    if desc_match:
                        params[param_name] = desc_match
        return params
    
    def _type_mapping(self, dtype):
        if dtype == float:
            return "number"
        elif dtype == int:
            return "integer"
        elif dtype == str:
            return "string"
        elif getattr(dtype, '__origin__', None) is Literal:
            return list(dtype.__args__)
        elif re.match(r"<module '(.+)' from", str(dtype)) is not None:
            match = re.match(r"<module '(.+)' from", str(dtype)).group()
            string = match.split(" ")[1].replace("'", "")
            return string
        elif re.match(r"<class '(.+)'>", str(dtype)) is not None:
            match = re.match(r"<class '(.+)'>", str(dtype)).group()
            string = match.split(" ")[1].replace("'", "")
            return string
        else:
            return str(dtype)
