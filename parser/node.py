from lexer import LexerToken, TokenType
import enum

class NodeType(enum.Enum):
    BinOp = 0
    Number = 1
    UnaryOp = 2
    Block = 3
    Assign = 4
    Variable = 5

class AstNode():
    def __init__(self, type, token):
        self.type = type
        self.token = token
    def __str__(self):
        return "AstNode[{0}, {1}]".format(self.type, self.token)
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

class NodeAssign(AstNode):
    def __init__(self, left, token, right):
        self.type = NodeType.Assign
        self.left = left
        self.token = token
        self.right = right

class NodeVariable(AstNode):
    def __init__(self, token):
        self.type = NodeType.Variable
        self.token = token
        self.value = token.value
