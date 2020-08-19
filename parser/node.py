from lexer import LexerToken, TokenType
from enum import Enum, auto

class NodeType(Enum):
    Empty    = auto()
    BinOp    = auto()
    Number   = auto()
    String   = auto()
    UnaryOp  = auto()
    Block    = auto()
    Assign   = auto()
    Variable = auto()
    Type     = auto()
    Declare  = auto()
    Call     = auto()
    Import   = auto()
    IfStatement  = auto()
    ArgumentList = auto()
    FunctionReturn     = auto()
    FunctionExpression = auto()
    TypeExpression   = auto()
    ObjectExpression = auto()
    MemberExpression = auto()

class AstNode():
    location = (0, 0)
    def __init__(self, type, token):
        self.type = type
        self.token = token
        self.location = token.location
    def __str__(self):
        try:
            return "AstNode[{0}, {1}]".format(self.type.name, self.token)
        except:
            return "AstNode[{0}]".format(self.type.name)
            
    def __repr__(self):
        return self.__str__()
        
class NodeNone(AstNode):
    def __init__(self, token):
        AstNode.__init__(self, NodeType.Empty, token)

# Binary op node; LEFT [+-*/] RIGHT
class NodeBinOp(AstNode):
    def __init__(self, left, token, right):
        AstNode.__init__(self, NodeType.BinOp, token)
        self.left = left
        self.token = token
        self.right = right

class NodeNumber(AstNode):
    def __init__(self, token):
        AstNode.__init__(self, NodeType.Number, token)
        self.token = token
        # int(..., 0) for guessing hexadecimal, float, etc.
        self.value = int(token.value, 0)
        
class NodeString(AstNode):
    def __init__(self, token):
        AstNode.__init__(self, NodeType.String, token)
        self.value = str(token.value)[1:-1]

# Unary node; switches signage for values, '!' operator
class NodeUnaryOp(AstNode):
    def __init__(self, token, expression):
        AstNode.__init__(self, NodeType.UnaryOp, token)
        self.token = token
        self.expression = expression

# Block node; parent to multiple nodes
class NodeBlock(AstNode):
    def __init__(self, token):
        AstNode.__init__(self, NodeType.Block, token)
        self.children = []

# Type node; Holds type info for variable
class NodeVarType(AstNode):
    def __init__(self, token):
        AstNode.__init__(self, NodeType.Type, token)
        self.token = token

    @property
    def is_type_type(self):
        return self.token.value == 'type'

# Declare node; declare variable or function
class NodeDeclare(AstNode):
    def __init__(self, type, name, value):
        AstNode.__init__(self, NodeType.Declare, name)
        self.type_node = type
        self.name = name
        self.value = value
        
class NodeImport(AstNode):
    def __init__(self, filename, source_location):
        AstNode.__init__(self, NodeType.Import, filename)
        self.children = []
        self.source_location = source_location

class NodeCall(AstNode):
    def __init__(self, lhs, argument_list):
        AstNode.__init__(self, NodeType.Call, lhs.token)
        self.lhs = lhs
        self.argument_list = argument_list

# Assignment node; Var = Value
class NodeAssign(AstNode):
    def __init__(self, lhs, value):
        AstNode.__init__(self, NodeType.Assign, value)
        self.lhs = lhs
        self.value = value

# Variable node; request value of variable
class NodeVariable(AstNode):
    def __init__(self, token):
        AstNode.__init__(self, NodeType.Variable, token)
        self.token = token
        self.value = token.value
        
class NodeIfStatement(AstNode):
    def __init__(self, expr, block, else_block):
        AstNode.__init__(self, NodeType.IfStatement, expr.token)
        self.expr = expr
        self.block = block
        self.else_block = else_block

class NodeArgumentList(AstNode):
    def __init__(self, arguments, token):
        AstNode.__init__(self, NodeType.ArgumentList, token)
        self.arguments = arguments

class NodeFunctionExpression(AstNode):
    def __init__(self, argument_list, block):
        AstNode.__init__(self, NodeType.FunctionExpression, block)
        self.argument_list = argument_list
        self.block = block
        
class NodeFunctionReturn(AstNode):
    def __init__(self, value_node, token):
        AstNode.__init__(self, NodeType.FunctionReturn, token)
        self.value_node = value_node

class NodeTypeExpression(AstNode):
    def __init__(self, name, members):
        # members are var decls
        self.type = NodeType.TypeExpression
        self.name = name
        self.members = members

class NodeObjectExpression(AstNode):
    def __init__(self, members):
        # members are var decls
        self.type = NodeType.ObjectExpression
        self.members = members

class NodeMemberExpression(AstNode):
    def __init__(self, lhs, identifier):
        self.type = NodeType.MemberExpression
        self.lhs = lhs
        self.identifier = identifier
