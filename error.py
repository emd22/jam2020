from enum import Enum, auto


class ErrorType(Enum):
    Syntax = auto()
    DoesNotExist = auto()

class Error():
    def __init__(self, type, location, message):
        self.type = type
        self.message = message
        self.location = location
    def __repr__(self):
        return "[{}:{}] {} error: {}".format(self.location[0], self.location[1], self.type, self.message)
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
