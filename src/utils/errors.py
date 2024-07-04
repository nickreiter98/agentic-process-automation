class ModellingError(Exception):
    def __init__(self):
        self.message = "The provided textual workflow could not be modelled"
        super().__init__(self.message)

    def __str__(self):
        return self.message
    
class PythonCodeExtractionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message
    
class FunctionSelectorError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message
    
class ParameterAssignatorError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message
    
class TaskExecutionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message
    
class DecisionMakingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message
    
class FunctionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message