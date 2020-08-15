from enum import Enum, auto
from parser.node import NodeType, NodeFunctionExpression

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
        if self.node != None:
            return "Function[{}, statements:{}]".format(self.name, len(self.node.children))
        else:
            return "Function[{}]".format(self.name)
    __str__ = __repr__
    
class BuiltinFunction(Function):
    def __init__(self, name, return_type, return_val):
        Function.__init__(self, name, return_type, None)

class Variable():
    def __init__(self, name, vtype, value):
        self.name = name
        self.value = 0

        if (type(value) is NodeFunctionExpression):
            self.value = Function(name, vtype, value)
        else:
            self.value = value
            
        self.type = vtype
        print("define [name:'{}' type:{}] as '{}'".format(name, vtype, value))
