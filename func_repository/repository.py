import inspect
import func_repository.descriptions as desc

class Repository:
    def __init__(self):
        self.functions = self._get_functions()

    def _get_functions(self):
        ls_func = []    
    
        for name, obj in inspect.getmembers(desc):
            if inspect.isfunction(obj) and name.startswith('d_'):
                ls_func.append(obj)

        return ls_func