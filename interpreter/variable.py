from enum import Enum, auto
from parser.node import NodeType, NodeFunctionExpression
from interpreter.typing.basic_type import BasicType
from interpreter.function import Function
from interpreter.basic_value import BasicValue

class VariableType(Enum):
    Auto     = 'auto'
    Int      = 'int'
    String   = 'str'
    Any      = 'any'
    Function = 'func'
    Type     = 'type'
    
    Array = auto()
    Object = auto() # Class, data structure, etc.

# class Variable(BasicValue):
#     def __init__(self, name, vtype, value):
#         BasicValue.__init__(self, value)
#         self.name = name
#         self.value = 0

#         if (type(value) is NodeFunctionExpression):
#             self.value = Function(name, vtype, value)
#         else:
#             self.value = value
            
#         self.type = vtype

#     def clone(self):
#         return Variable(self.name, self.vtype, self.value)