from parser import *
from lexer import TokenType
    
class Interpreter():
    def __init__(self, parser):
        self.parser = parser
        self.ast = parser.parse()
        
    def interpret(self):
        return self.visit(self.ast)
        
    def visit(self, node):
        if node.type == NodeType.BinOp:
            return self.visit_binop(node)
        elif node.type == NodeType.Number:
            return self.visit_number(node)
        elif node.type == NodeType.UnaryOp:
            return self.visit_unaryop(node)
        else:
            raise Exception('Visitor function not defined')
            
    def visit_binop(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.token.type == TokenType.Plus:
            return left+right
        elif node.token.type == TokenType.Minus:
            return left-right
        elif node.token.type == TokenType.Multiply:
            return left*right
        elif node.token.type == TokenType.Divide:
            return left/right
        return 0
        
    def visit_number(self, node):
        return node.value
    
    def visit_unaryop(self, node):
        val = self.visit(node.expression)
        if node.token.type == TokenType.Plus:
            return +val
        elif node.token.type == TokenType.Minus:
            return -val
            
    
