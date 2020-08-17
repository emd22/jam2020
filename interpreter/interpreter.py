from parser.parser import Parser
from parser.node import AstNode, NodeType
from interpreter.scope import *
from interpreter.stack import Stack
from interpreter.function import BuiltinFunction
from interpreter.typing.basic_type import BasicType
from interpreter.basic_object import BasicObject, RootObject
from parser.node import NodeVariable, NodeMemberExpression
from lexer import TokenType, LexerToken

from error import errors, ErrorType, Error 

def _print_object(interpreter, obj):
    obj_str = repr(obj)

    if isinstance(obj, BasicObject):
        meth = obj.lookup_member('__repr__')

        if meth is not None:
            obj_str = interpreter.call_function_expression(meth.value)

    print(obj_str)
    
def builtin_varinfo(arguments):
    interpreter = arguments[0]
    var = interpreter.current_scope.find_variable(arguments[2])
    print(f"Variable '{var.name}' type: {var.type.name}")
    

def builtin_printn(arguments):
    interpreter = arguments[0]

    for arg in arguments[2:]:
        _print_object(interpreter, arg)

    return 0
    
def builtin_return(arguments):
    interpreter = arguments[0]
    node  = arguments[1]
    value = arguments[2]
    
    interpreter.stack.push(value)
    
def builtin_type_compare(arguments):
    interpreter = arguments[0]
    node = arguments[1]
    target = arguments[2]
    type_obj = arguments[3]

    if not isinstance(target, BasicObject):
        interpreter.error(node, ErrorType.TypeError, 'argument 1 ({}) is not a BasicObject, cannot perform typecheck'.format(target))
        return None

    if not isinstance(type_obj, BasicType):
        interpreter.error(node, ErrorType.TypeError, 'argument 2 ({}) is not a BasicType, cannot perform typecheck'.format(type_obj))

    if target.satisfies_type(type_obj):
        return 1
    else:
        return 0

class Interpreter():
    def __init__(self, parser):
        self.parser = parser
        self.ast = parser.parse()
        self.selected_parser = self.parser
        # declare scopes + global scope
        self.stack = Stack()
        self.builtins = [
            BuiltinFunction("__intern_print__", None, builtin_printn),
            BuiltinFunction("__intern_type_compare__", None, builtin_type_compare),
            BuiltinFunction("__intern_varinfo__", None, builtin_varinfo),
            BuiltinFunction("return", None, builtin_return)
        ]
        
        self.global_scope = Scope(None)
        self._top_level_scope = None

    @property
    def current_scope(self):
        if self._top_level_scope is not None:
            return self._top_level_scope

        return self.global_scope

    def open_scope(self):
        #print("Open Scope")
        self._top_level_scope = Scope(self.current_scope)

    def close_scope(self):
        if self.current_scope == self.global_scope:
            raise Exception('cannot close global scope!')
        #print("Close scope")
        self._top_level_scope = self.current_scope.parent

        return self.current_scope
        
    def interpret(self):
        return self.visit(self.ast)
        
    def error(self, node, type, message):
        errors.push_error(Error(type, node.location, message, self.selected_parser.filename))
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
        
        defvar = self.current_scope.find_variable(node.name.value, limit=True)
        if defvar != None:
            self.error(node, ErrorType.MultipleDefinition, "multiple definition of '{}'".format(node.name.value))
   
        self.current_scope.declare_variable(node.name.value, vtype)
        val = self.visit(node.value)
        return val
    
    def visit_Import(self, node):
        self.selected_parser = node.parser
        for child in node.children:
            self.visit(child)
        self.selected_parser = self.parser
    
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

        for child in node.children:
            self.visit(child)

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

        # TODO: Do not iterate builtins before local vars -- allow them to be overwritten.
        # instead, have the interpreter declare the builtins the same way we'd do locals,
        # but assign them to the appropriate BuiltinFunction objects.
        if isinstance(node.lhs, NodeVariable):
            # check builtins.
            for builtin in self.builtins:
                if builtin.name == node.lhs.value:
                    target = builtin
                    break

        if target is None:
            target = self.visit(node.lhs) # TODO: turn into general expression, not just vars.

        if target is not None:
            if isinstance(target, BuiltinFunction):
                arguments = []

                # built-in function
                for arg in node.argument_list.arguments:
                    arguments.append(self.visit(arg))

                return builtin.call([self, node, *arguments])
            else:
                # user-defined function
                # push arguments to stack
                for arg in node.argument_list.arguments:
                    self.stack.push(arg)
                
                
                #old_scope = self._top_level_scope
                #self._top_level_scope = old_scope.parent
                value = self.call_function_expression(target)
                #self._top_level_scope = old_scope
        else:
            self.error(node, ErrorType.TypeError, 'invalid call: {} ({}) is not a built-in or user-defined function'.format(node.var.value, target))
        value = self.stack.pop()
        return value

    def walk_variable(self, node):
        var = self.current_scope.find_variable(node.value)

        if var is None:
            self.error(node, ErrorType.DoesNotExist, "Referencing undefined variable '{}'".format(node.value))
            return None

        return var
            
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
            self.current_scope.find_variable(argument.name.value).value = self.visit(value)

    def visit_FunctionExpression(self, node):
        pass

    def call_function_expression(self, node):
        # create our scope before block so argument variables are contained
        self.open_scope()
        # visit our arguments
        self.visit(node.argument_list)
        # self.visit would normally be used here, but we need create_scope
        self.visit_Block(node.block, create_scope=False)
        # done, close scope
        self.close_scope()

    def visit_TypeExpression(self, node):
        obj_expr = self.visit_object_expression(node)

        return BasicType(node.name, obj_expr.parent, obj_expr.members)

    def visit_ObjectExpression(self, node):
        members = {}

        # open scope for members
        self.open_scope()

        for member_decl in node.members:
            value = self.visit(member_decl)

            members[member_decl.name.value] = value

        # close scope for members
        self.close_scope()

        return BasicObject(parent=RootObject, members=members)

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
    
