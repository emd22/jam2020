from lexer import LexerToken, TokenType
from enum import Enum, auto

class NodeType(Enum):
    BinOp = auto()
    Number = auto()
    UnaryOp = auto()
    Block = auto()
    Assign = auto()
    Variable = auto()
    Type = auto()
    Declare = auto()

class AstNode():
    def __init__(self, type, token):
        self.type = type
        self.token = token
    def __str__(self):
        try:
            return "AstNode[{0}, {1}]".format(self.type, self.token)
        except:
            return "AstNode[{0}]".format(self.type)
            
    def __repr__(self):
        return self.__str__()
        
class NodeNone(AstNode):
    pass
      
class NodeBinOp(AstNode):
    def __init__(self, left, token, right):
        self.type = NodeType.BinOp
        self.left = left
        self.token = token
        self.right = right
        
class NodeNumber(AstNode):
    def __init__(self, token):
        self.type = NodeType.Number
        self.token = token
        self.value = int(token.value)

class NodeUnaryOp(AstNode):
    def __init__(self, token, expression):
        self.type = NodeType.UnaryOp
        self.token = token
        self.expression = expression

class NodeBlock(AstNode):
    def __init__(self):
        self.type = NodeType.Block
        self.children = []
        
class NodeVarType(AstNode):
    def __init__(self, token):
        self.type = NodeType.Type
        self.token = token

class NodeDeclare(AstNode):
    def __init__(self, type, name, value):
        self.type = NodeType.Declare
        self.type_node = type
        self.name = name
        self.value = value

class NodeAssign(AstNode):
    def __init__(self, var, value):
        self.type = NodeType.Assign
        self.var = var
        self.value = value

class NodeVariable(AstNode):
    def __init__(self, token):
        self.type = NodeType.Variable
        self.token = token
        self.value = token.value

