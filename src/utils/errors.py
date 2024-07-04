class ModellingError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"ModellingError: {self.message}"
    
class PythonCodeExtractionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message
    
class FunctionSelectorError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"FunctionSelectorError: {self.message}"

class ParameterAssignatorError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"ParameterAssignationError: {self.message}"
    
class DecisionMakingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"DecisionMakingError: {self.message}"
    
class FunctionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"FunctionError: {self.message}"