import functools
import inspect
import re

from typing import Literal


def convert_function_to_json_representation(func, format: str = "normal"):
    # Check if the function is a functools.partial
    if isinstance(func, functools.partial) or isinstance(func, functools.partialmethod):
        fixed_args = func.keywords
        _func = func.func
        if isinstance(func, functools.partial) and (
            fixed_args is None or fixed_args == {}
        ):
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
    func_description = "".join(
        [line for line in func_doc.split("\n") if not line.strip().startswith(":")]
    )
    # parse the docstring to get the descriptions for each parameter in dict format
    param_details = extract_params(func_doc) if func_doc else {}
    # attach parameter types to params and exclude fixed args
    # get params
    params = {}
    for param_name in argspec.args:
        if param_name not in fixed_args.keys():
            params[param_name] = {
                "description": param_details.get(param_name) or "",
                "type": map_type(argspec.annotations.get(param_name, type(None))),
            }
    # calculate required parameters excluding fixed args
    # _required = [arg for arg in argspec.args if arg not in fixed_args]
    _required = [i for i in argspec.args if i not in fixed_args.keys()]
    sig = inspect.signature(_func)
    requ_params = sig.parameters
    _required = [
        name
        for name, param in requ_params.items()
        if param.default == inspect.Parameter.empty
    ]

    if format == "normal":
        return {
            "name": func_name,
            "description": func_description,
            "parameters": {"type": "object", "properties": params},
            "required": _required,
        }
    elif format == "arguments":
        return {"parameters": params, "required": _required}


def extract_params(doc_str: str):
    # split doc string by newline, skipping empty lines
    params_str = [line for line in doc_str.split("\n") if line.strip()]
    params = {}
    for line in params_str:
        # we only look at lines starting with ':param'
        if line.strip().startswith(":param"):
            param_match = re.findall(r"(?<=:param )\w+", line)
            if param_match:
                param_name = param_match[0]
                desc_match = line.replace(f":param {param_name}:", "").strip()
                # if there is a description, store it
                if desc_match:
                    params[param_name] = desc_match
    return params


def map_type(dtype):
    if dtype == float:
        return "number"
    elif dtype == int:
        return "integer"
    elif dtype == str:
        return "string"
    elif getattr(dtype, "__origin__", None) is Literal:
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
