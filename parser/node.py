from lexer import LexerToken, TokenType
from enum import Enum, auto

class NodeType(Enum):
    BinOp = auto()
    Number = auto()
    String = auto()
    UnaryOp = auto()
    Block = auto()
    Assign = auto()
    Variable = auto()
    Type = auto()
    Declare = auto()
    Call = auto()
    IfStatement = auto()
    ArgumentList = auto()
    FunctionExpression = auto()

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

# Binary op node; LEFT [+-*/] RIGHT
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

# Unary node; switches signage for values
class NodeUnaryOp(AstNode):
    def __init__(self, token, expression):
        self.type = NodeType.UnaryOp
        self.token = token
        self.expression = expression

# Block node; parent to multiple nodes
class NodeBlock(AstNode):
    def __init__(self):
        self.type = NodeType.Block
        self.children = []

# Type node; Holds type info for variable
class NodeVarType(AstNode):
    def __init__(self, token):
        self.type = NodeType.Type
        self.token = token

# Declare node; declare variable or function
class NodeDeclare(AstNode):
    def __init__(self, type, name, value):
        self.type = NodeType.Declare
        self.type_node = type
        self.name = name
        self.value = value

class NodeCall(AstNode):
    def __init__(self, var, params):
        self.type = NodeType.Call
        self.var = var
        self.params = params

# Assignment node; Var = Value
class NodeAssign(AstNode):
    def __init__(self, var, value):
        self.type = NodeType.Assign
        self.var = var
        self.value = value

# Variable node; request value of variable
class NodeVariable(AstNode):
    def __init__(self, token):
        self.type = NodeType.Variable
        self.token = token
        self.value = token.value
        
class NodeIfStatement(AstNode):
    def __init__(self, expr, block, else_block):
        self.type = NodeType.IfStatement
        self.expr = expr
        self.block = block
        self.else_block = else_block

class NodeArgumentList(AstNode):
    def __init__(self, arguments):
        self.type = NodeType.ArgumentList
        self.arguments = arguments

class NodeFunctionExpression(AstNode):
    def __init__(self, argument_list, block):
        self.type = NodeType.FunctionExpression
        self.argument_list = argument_list
        self.block = block