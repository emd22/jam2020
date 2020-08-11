from enum import Enum, auto

class VariableType(Enum):
    Auto = 'auto'
    Int = 'int'
    String = 'str'
    Any = 'any'
    Function = 'func'
    
    Array = auto()
    Object = auto() # Class, data structure, etc.

class Variable():
    def __init__(self, name, vtype, value):
        self.name = name
        self.value = value
        self.type = vtype
        print("define '{}' as '{}'".format(name, value))
