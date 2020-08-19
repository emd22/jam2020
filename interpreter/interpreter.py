from parser.parser import Parser
from parser.node import AstNode, NodeType, NodeFunctionReturn
from interpreter.scope import *
from interpreter.stack import Stack
from interpreter.function import BuiltinFunction
from interpreter.typing.basic_type import BasicType
from interpreter.basic_object import BasicObject
from interpreter.basic_value import BasicValue
from interpreter.env.globals import Globals
from interpreter.variable import VariableType
from parser.node import NodeVariable, NodeMemberExpression
from lexer import TokenType, LexerToken

from error import errors, ErrorType, Error 


class Interpreter():
    def __init__(self, parser):
        self.parser = parser
        self.ast = parser.parse()
        self.selected_parser = self.parser
        # declare scopes + global scope
        self.stack = Stack()
        
        self.global_scope = Scope(None)
        self._top_level_scope = None

        Globals().apply_to_scope(self.global_scope)

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
        location = None

        if node is not None:
            location = node.location

        errors.push_error(Error(type, location, message, self.selected_parser.filename))
        errors.print_errors()
        quit()
        
    def visit(self, node):
        caller_name = "visit_{}".format(str(node.type.name))
        caller = getattr(self, caller_name)
        return caller(node)
            
    def visit_BinOp(self, node):
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
            
        elif node.token.type == TokenType.BitwiseOr:
            return (left | right)
        elif node.token.type == TokenType.BitwiseAnd:
            return (left & right)
            
        return 0
        
    def visit_Type(self, node):
        pass
    
    def visit_Declare(self, node):
        if node.type_node != None:
            # set type to VariableType(type_node)
            vtype = VariableType(node.type_node.token.value)
        else:
            # no type node attached, default to VariableType.any
            vtype = VariableType.Any

        if self.current_scope.find_variable_info(node.name.value, limit=True) != None:
            self.error(node, ErrorType.MultipleDefinition, "multiple definition of '{}'".format(node.name.value))
   
        self.current_scope.declare_variable(node.name.value, vtype)
        val = self.visit(node.value)
        return val
    
    def visit_Import(self, node):
        # the imported file is already lexed and parsed from the parser, so this
        # acts like a block and visits the statements inside. This means that if we
        # import inside a function, any variables should only be available to that
        # scope.
        self.selected_parser = node.parser
        for child in node.children:
            self.visit(child)
        self.selected_parser = self.parser
    
    def visit_FunctionReturn(self, node):
        value = self.visit(node.value_node)
        self.stack.push(value)
    
    def visit_Number(self, node):
        return node.value
    
    def visit_String(self, node):
        return node.value
    
    def visit_UnaryOp(self, node):
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
            
    def visit_Block(self, node, create_scope=True):
        if create_scope:
            self.open_scope()
        
        # visit each statement in block
        for child in node.children:
            self.visit(child)
            if type(child) == NodeFunctionReturn:
                break
            
        if create_scope:
            self.close_scope()
        
    def visit_Assign(self, node):
        if node.value.type == NodeType.FunctionExpression:
            value = node.value
        else:
            value = self.visit(node.value)

        if isinstance(node.lhs, NodeVariable):
            target = self.walk_variable(node.lhs)
            target.assign_value(value)

        elif isinstance(node.lhs, NodeMemberExpression):
            (target, member) = self.walk_member_expression(node.lhs)

            if not isinstance(target, NodeMemberExpression):
                self.error(node, ErrorType.TypeError, 'member expression not assignable')
                return None

            # TODO: type contract checking?
            # objects that have a type tagged on require undergoing validation of the property type
            # before assigning will work successfully?
            target.assign_member(member.name, value)
        else:
            self.error(node, ErrorType.TypeError, 'cannot assign {}'.format(node.lhs))

            return None
        
        return value
    
    def visit_Call(self, node):
        #print("Call function '{}'".format(node.var.value))

        target = None
        return_value = 0

        # TODO: Do not iterate builtins before local vars -- allow them to be overwritten.
        # instead, have the interpreter declare the builtins the same way we'd do locals,
        # but assign them to the appropriate BuiltinFunction objects.
        # if isinstance(node.lhs, NodeVariable):
        #     # check builtins.
        #     for builtin in self.builtins:
        #         if builtin.name == node.lhs.value:
        #             target = builtin
        #             break

        if target is None:
            target = self.visit(node.lhs) # TODO: turn into general expression, not just vars.

        if target is not None:
            this_value = None

            # for `a.b()`, pass in `a` as the this value.
            if isinstance(node.lhs, NodeMemberExpression):
                this_value = self.visit(node.lhs.lhs)

            # if a built-in function exists, call it
            if isinstance(target, BuiltinFunction):
                return_value = self.call_builtin_function(target, this_value, node.argument_list.arguments, node)
            # user-defined function
            else:               
                # push arguments to stack
                for arg in node.argument_list.arguments:
                    self.stack.push(arg)
                
                self.call_function_expression(target)
                # the return value is pushed onto the stack at end of block or return
                # statement. Pop it off and return as a value
                return_value = self.stack.pop()
        else:
            self.error(node, ErrorType.TypeError, 'invalid call: {} ({}) is not a built-in or user-defined function'.format(node.var.value, target))

        return return_value

    def walk_variable(self, node):
        var = self.current_scope.find_variable_info(node.value)

        if var is None:
            self.error(node, ErrorType.DoesNotExist, "Referencing undefined variable '{}'".format(node.value))
            return None

        return var.value_wrapper
            
    def visit_Variable(self, node):
        var = self.walk_variable(node)

        if var is not None:
            return var.value

        return None
        
    def visit_IfStatement(self, node):
        expr_result = self.visit(node.expr)

        # todo this should be changed to a general purpose 'is true' check
        if expr_result != 0:
            self.visit_Block(node.block)
        elif node.else_block is not None:
            self.visit_Block(node.else_block)
        
    def visit_ArgumentList(self, node):
        # read arguments backwards as values are popped from stack
        for argument in reversed(node.arguments):
            # retrieve value
            value = self.stack.pop()
            # declare variable
            self.visit_Declare(argument)
            # TODO: clean up
            # set variable to passed in value
            self.current_scope.set_variable(argument.name.value, self.visit(value))

    def visit_FunctionExpression(self, node):
        pass

    def call_builtin_function(self, fun, this_object, arguments, node):
        args = []

        # built-in function
        for arg in arguments:
            args.append(self.visit(arg))

        basic_value_result = fun.call([self, this_object, *args])

        if not isinstance(basic_value_result, BasicValue):
            self.error(node, ErrorType.TypeError, 'expected method {} to return an instance of BasicValue, got {}'.format(fun, basic_value_result))
            return None

        return basic_value_result

    def call_function_expression(self, node):
        # create our scope before block so argument variables are contained
        self.open_scope()
        # visit our arguments
        self.visit(node.argument_list)
        # self.visit would normally be used here, but we need create_scope
        self.visit_Block(node.block, create_scope=False)
        
        # check if block contains a return statement
        for child in node.block.children:
            if type(child) == NodeFunctionReturn:
                break
        else:
            # no return statement, push return code 0 to the stack
            if type(child) != NodeFunctionReturn:
                self.stack.push(0)
            
        # done, close scope
        self.close_scope()

    def visit_TypeExpression(self, node):
        obj_expr = self.visit_object_expression(node)

        return BasicType(obj_expr.parent, obj_expr.members)

    def visit_ObjectExpression(self, node):
        members = {}

        # open scope for members
        self.open_scope()

        for member_decl in node.members:
            value = self.visit(member_decl)

            members[member_decl.name.value] = value

        # close scope for members
        self.close_scope()

        # TODO make parent be the global `Object` type.
        return BasicObject(parent=None, members=members)

    def walk_member_expression(self, node):
        target = self.visit(node.lhs)

        if target is None:
            self.error(node, ErrorType.TypeError, 'invalid member access: {} has no member {}'.format(target, node.rhs.name))
            return None

        if not isinstance(target, BasicObject):
            self.error(node, ErrorType.TypeError, 'invalid member access: target {} is not a BasicObject'.format(target))
            return None

        member = target.lookup_member(node.identifier.value)

        if member is None:
            self.error(node, ErrorType.TypeError, 'object {} has no direct or inherited member `{}`'.format(target, node.identifier.value))

        return (target, member)

    def visit_MemberExpression(self, node):
        return self.walk_member_expression(node)[1].value
        
    def visit_Empty(self, node):
        pass
    
