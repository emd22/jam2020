from enum import Enum, auto
from parser.node import NodeType, NodeFunctionExpression
from interpreter.typing.basic_type import BasicType
from interpreter.function import Function

class VariableType(Enum):
    Auto     = 'auto'
    Int      = 'int'
    String   = 'str'
    Any      = 'any'
    Function = 'func'
    Type     = 'type'
    
    Array = auto()
    Object = auto() # Class, data structure, etc.

INT_TYPE = BasicType('int', None, {}, True)
STRING_TYPE = BasicType('str', None, {}, True)
ANY_TYPE = BasicType('any', None, {}, True)
FUNC_TYPE = BasicType('func', None, {}, True)

class Variable():
    def __init__(self, name, vtype, value):
        self.name = name
        self.value = 0

        if (type(value) is NodeFunctionExpression):
            self.value = Function(name, vtype, value)
        else:
            self.value = value
            
        self.type = vtype

    def assign_value(self, value):
        # TODO: type assertions
        self.value = value