from enum import Enum, auto
from util import LogColour

class ErrorType(Enum):
    Syntax = auto()
    DoesNotExist = auto()
    TypeError = auto()
    MultipleDefinition = auto()

class Error():
    def __init__(self, type, location, message, filename):
        self.type = type
        self.filename = filename
        self.message = message
        self.location = location
    def __repr__(self):
        nstr = f"{self.filename}:{self.location[1]}:{self.location[0]}: {LogColour.Error}{self.type.name} error:{LogColour.Default}"
        return f"{LogColour.Bold}{nstr}{LogColour.Default} {self.message}"
    __str__ = __repr__
        
class ErrorList():
    def __init__(self):
        self.errors = []
    
    def push_error(self, error):
        self.errors.append(error)
        
    def print_errors(self):
        for error in self.errors:
            print(error)
        
    def get_errors(self):
        return self.errors
        
errors = ErrorList()
