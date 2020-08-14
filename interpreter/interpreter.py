from parser.parser import Parser
from parser.node import AstNode, NodeType
from interpreter.scope import *
from lexer import TokenType

class Interpreter():
    def __init__(self, parser):
        self.parser = parser
        self.ast = parser.parse()
        # declare scopes + global scope
        self.scopes = [Scope()]
        
    def interpret(self):
        return self.visit(self.ast)
        
    def visit(self, node):
        if node.type == NodeType.BinOp:
            return self.visit_binop(node)
        elif node.type == NodeType.Number:
            return self.visit_number(node)
        elif node.type == NodeType.UnaryOp:
            return self.visit_unaryop(node)
        elif node.type == NodeType.Block:
            return self.visit_block(node)
        elif node.type == NodeType.Assign:
            return self.visit_assign(node)
        elif node.type == NodeType.Variable:
            return self.visit_variable(node)
        elif node.type == NodeType.Type:
            return self.visit_type(node)
        elif node.type == NodeType.Declare:
            return self.visit_declare(node)
        elif node.type == NodeType.Call:
            return self.visit_call(node)
        elif node.type == NodeType.IfStatement:
            return self.visit_if_statement(node)
        else:
            raise Exception('Visitor function for {} not defined'.format(node.type))
            
    def visit_binop(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.token.type == TokenType.Plus:
            return left + right
        elif node.token.type == TokenType.Minus:
            return left - right
        elif node.token.type == TokenType.Multiply:
            return left * right
        elif node.token.type == TokenType.Divide:
            return left // right
        return 0
        
    def visit_type(self, node):
        pass 
    
    def visit_declare(self, node):
        val = self.visit(node.value)
        if node.type_node != None:
            # set type to VariableType(type_node)
            vtype = VariableType(node.type_node.token.value)
        else:
            # no type node attached, default to VariableType.any
            vtype = VariableType.Any
            
        self.scopes[0].declare_variable(node.name.value, vtype, val)
        return val
    
    def visit_number(self, node):
        return node.value
    
    def visit_unaryop(self, node):
        val = self.visit(node.expression)
        if node.token.type == TokenType.Plus:
            return +val
        elif node.token.type == TokenType.Minus:
            return -val
            
    def visit_block(self, node):
        for child in node.children:
            self.visit(child)
        
    def visit_assign(self, node):
        var_name = node.var.value
        if node.value.type == NodeType.Block:
            value = node.value
        else:
            value = self.visit(node.value)
        print("Set {} to {}".format(var_name, value))
        var = self.scopes[0].find_variable(var_name)
        if var != None:
            var.value = value
        return value
    
    def visit_call(self, node):
        print("Call function '{}'".format(node.var.value))
        var = self.scopes[0].find_variable(node.var.value)
        if var != None:
            if type(var.value) != Function:
                raise Exception('calling wrong variable type')
            value = self.visit(var.value.node)
        else:
            value = 0
        return value
            
    def visit_variable(self, node):
        print("Visit variable {}".format(node.value))
        var = self.scopes[0].find_variable(node.value)
        if var != None:
            value = var.value
        else:
            value = 0
        return value
        
    def visit_if_statement(self, node):
        expr_result = self.visit(node.expr)

        # todo this should be changed to a general purpose 'is true' check
        if expr_result != 0:
            self.visit_block(node.block)
        elif node.else_block is not None:
            self.visit_block(node.else_block)
        
    
    def visit_none(self, node):
        pass
        
