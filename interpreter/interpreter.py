from parser.parser import Parser
from parser.node import AstNode, NodeType
from interpreter.scope import *
from interpreter.stack import Stack
from lexer import TokenType, LexerToken

from error import errors, ErrorType, Error 


class Interpreter():
    def __init__(self, parser, filename):
        self.parser = parser
        self.ast = parser.parse()
        # declare scopes + global scope
        self.filename = filename
        self.stack = Stack()
        self.global_scope = Scope(None)
        self._top_level_scope = None

    @property
    def current_scope(self):
        if self._top_level_scope is not None:
            return self._top_level_scope

        return self.global_scope

    def open_scope(self):
        self._top_level_scope = Scope(self.current_scope)

    def close_scope(self):
        if self.current_scope == self.global_scope:
            raise Exception('cannot close global scope!')

        self._top_level_scope = self.current_scope.parent

        return self.current_scope
        
    def interpret(self):
        return self.visit(self.ast)
        
    def error(self, node, type, message):
        errors.push_error(Error(type, node.location, message, self.filename))
        errors.print_errors()
        quit()
        
    def visit(self, node):
        if node.type == NodeType.Empty:
            pass
        elif node.type == NodeType.BinOp:
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
        elif node.type == NodeType.ArgumentList:
            return self.visit_argument_list(node)
        elif node.type == NodeType.FunctionExpression:
            return self.visit_function_expression(node)
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
        if node.type_node != None:
            # set type to VariableType(type_node)
            vtype = VariableType(node.type_node.token.value)
        else:
            # no type node attached, default to VariableType.any
            vtype = VariableType.Any
   
        self.current_scope.declare_variable(node.name.value, vtype)
        val = self.visit(node.value)
        return val
        
    
    def visit_number(self, node):
        return node.value
    
    def visit_unaryop(self, node):
        val = self.visit(node.expression)
        
        if node.token.type == TokenType.Plus:
            return +val
        elif node.token.type == TokenType.Minus:
            return -val
        elif node.token.type == TokenType.Not:
            if val == 0:
                return 1
            else:
                return 0
            
    def visit_block(self, node, create_scope=True):
        if create_scope:
            self.open_scope()

        for child in node.children:
            self.visit(child)

        if create_scope:
            self.close_scope()
        
    def visit_assign(self, node):
        var_name = node.var.value
        if node.value.type == NodeType.FunctionExpression:
            value = node.value
        else:
            value = self.visit(node.value)
    
        var = self.current_scope.find_variable(var_name)
        if var != None:
            var.value = value
        else:
            self.error(node, ErrorType.DoesNotExist, "Variable '{}' not defined in scope".format(var_name))
        print("Set {} to {}".format(var_name, value))
        return value
    
    def visit_call(self, node):
        print("Call function '{}'".format(node.var.value))
        var = self.current_scope.find_variable(node.var.value)
        if var != None:
            #if type(var) != Function:
            #    self.error(node, ErrorType.TypeError, 'Calling wrong variable type')

            # push arguments to stack
            for arg in node.argument_list.arguments:
                self.stack.push(arg)

            value = self.visit(var.value)
        else:
            value = 0
        return value
            
    def visit_variable(self, node):
        print("Visit variable {}".format(node.value))
        var = self.current_scope.find_variable(node.value)
        if var != None:
            value = var.value
        else:
            self.error(node, ErrorType.DoesNotExist, "Referencing undefined variable '{}'".format(node.value))
            value = 0
        return value
        
    def visit_if_statement(self, node):
        expr_result = self.visit(node.expr)

        # todo this should be changed to a general purpose 'is true' check
        if expr_result != 0:
            self.visit_block(node.block)
        elif node.else_block is not None:
            self.visit_block(node.else_block)
        
    def visit_argument_list(self, node):
        # read arguments backwards as values are popped from stack
        for argument in reversed(node.arguments):
            # retrieve value
            value = self.stack.pop()
            # declare variable
            self.visit_declare(argument)
            # TODO: clean up
            # set variable to passed in value
            self.current_scope.find_variable(argument.name.value).value = self.visit(value)

    def visit_function_expression(self, node):
        # create our scope before block so argument variables are contained
        self.open_scope()
        # visit our arguments
        self.visit(node.argument_list)
        # self.visit would normally be used here, but we need create_scope
        self.visit_block(node.block, create_scope=False)
        # done, close scope
        self.close_scope()

    def visit_none(self, node):
        pass
        
    
