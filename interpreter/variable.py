from enum import Enum, auto
from parser.node import NodeType, NodeBlock

class VariableType(Enum):
    Auto     = 'auto'
    Int      = 'int'
    String   = 'str'
    Any      = 'any'
    Function = 'func'
    
    Array = auto()
    Object = auto() # Class, data structure, etc.
    
class Function():
    def __init__(self, name, return_type, node):
        self.name = name
        self.return_type = return_type
        self.node = node
    def __repr__(self):
        return "Function[{}, statements:{}]".format(self.name, len(self.node.children))
    __str__ = __repr__

class Variable():
    def __init__(self, name, vtype, value):
        self.name = name
        self.value = 0
        
        if (type(value) is NodeBlock):
            self.value = Function(name, vtype, value)
        else:
            self.value = value
            
        self.type = vtype
        print("define [name:'{}' type:{}] as '{}'".format(name, vtype, value))
