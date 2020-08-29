from enum import Enum, auto
from util import LogColour

class InterpreterError(Exception):
    pass

class ErrorType(Enum):
    Syntax = auto()
    DoesNotExist = auto()
    TypeError = auto()
    MultipleDefinition = auto()
    ArgumentError = auto()
    MacroExpansionError = auto()

class Error():
    def __init__(self, type, location, message, filename):
        self.type = type
        self.filename = filename
        self.message = message
        self.location = location

    @property
    def location_filename(self):
        if self.filename is None:
            return '<none>'

        return self.filename

    @property
    def location_row(self):
        if self.location is None:
            return 0

        return self.location[1]

    @property
    def location_col(self):
        if self.location is None:
            return 0

        return self.location[0]

    def __repr__(self):
        nstr = f"{self.location_filename}:{self.location_row}:{self.location_col}: {LogColour.Error}{self.type.name} error:{LogColour.Default}"
        return f"{LogColour.Bold}{nstr}{LogColour.Default} {self.message}"
    __str__ = __repr__
        
class ErrorList():
    def __init__(self):
        self.errors = []

    def clear_errors(self):
        self.errors = []
    
    def push_error(self, error):
        self.errors.append(error)
        
    def print_errors(self):
        for error in self.errors:
            print(error)
        
    def get_errors(self):
        return self.errors

