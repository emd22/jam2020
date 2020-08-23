from parser.parser import Parser
from parser.node import AstNode, NodeType, NodeFunctionReturn
from parser.source_location import SourceLocation
from parser.node import *

from interpreter.scope import *
from interpreter.stack import Stack
from interpreter.function import BuiltinFunction
from interpreter.typing.basic_type import BasicType
from interpreter.basic_object import BasicObject
from interpreter.basic_value import BasicValue
from interpreter.env.globals import Globals
from interpreter.variable import VariableType
from interpreter.env.builtins import builtin_object_new
from lexer import TokenType, LexerToken

from error import InterpreterError, ErrorList, ErrorType, Error

class Interpreter():
    def __init__(self, source_location):
        self.source_location = source_location
        self.error_list = ErrorList()
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

    def error(self, node, type, message):
        location = None

        if node is not None:
            location = node.location

        self.error_list.push_error(Error(type, location, message, self.source_location.filename))
        self.error_list.print_errors()

        raise InterpreterError('Interpreter error')
        
    def visit(self, node):
        try:
            caller_name = "visit_{}".format(str(node.type.name))
            caller = getattr(self, caller_name)
        except:
            raise Exception('No visitor function defined for node {}'.format(node))

        return caller(node)
            
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        # TODO operator overloading by calling method on obj
        # Int method __add__ could just be a builtin method intern_int_add
        funstr = '__noop__'
        
        if node.token.type == TokenType.Plus:
            funstr = '__add__'
        elif node.token.type == TokenType.Minus:
            funstr = '__sub__'
        elif node.token.type == TokenType.Multiply:
            funstr = '__mul__'
        elif node.token.type == TokenType.Divide:
            funstr = '__div__'
            
        elif node.token.type == TokenType.BitwiseOr:
            return BasicValue(left.value | right.value)
        elif node.token.type == TokenType.BitwiseAnd:
            return BasicValue(left.value & right.value)
        elif node.token.type == TokenType.Spaceship:
            funstr = '__compare__'
        elif node.token.type == TokenType.LessThan:
            funstr = '__lt__'
        elif node.token.type == TokenType.LessThanEqual:
            funstr = '__lte__'
        elif node.token.type == TokenType.GreaterThan:
            funstr = '__gt__'
        elif node.token.type == TokenType.GreaterThanEqual:
            funstr = '__gte__'
        elif node.token.type == TokenType.Compare:
            return BasicValue(int(left.value == right.value))
        elif node.token.type == TokenType.NotCompare:
            return BasicValue(int(left.value != right.value))
            
        member_access_call_node = NodeCall(
            NodeMemberExpression(
                node.left,
                LexerToken(funstr, TokenType.Identifier),
                node.token
            ),
            NodeArgumentList(
                [node.right],
                node.token
            )
        )

        return self.visit(member_access_call_node)
        
    def visit_Type(self, node):
        pass
    
    def visit_Declare(self, node):

        # if node.type_node != None:
        #     # set type to VariableType(type_node)
        #     vtype = VariableType(node.type_node.token.value)
        # else:
        #     # no type node attached, default to VariableType.any
        #     vtype = VariableType.Any
        type_node_value = None # TODO default to Any or type of assignment

        if node.type_node is not None:
            type_node_value = self.visit(node.type_node)

        if self.current_scope.find_variable_info(node.name.value, limit=True) != None:
            self.error(node, ErrorType.MultipleDefinition, "multiple definition of '{}'".format(node.name.value))
   
        self.current_scope.declare_variable(node.name.value, type_node_value)
        val = self.visit(node.value)
        return val
    
    def visit_Import(self, node):
        # the imported file is already lexed and parsed from the parser, so this
        # acts like a block and visits the statements inside. This means that if we
        # import inside a function, any variables should only be available to that
        # scope.
        old_source_location = self.source_location
        self.source_location = node.source_location

        for child in node.children:
            self.visit(child)

        self.source_location = old_source_location
    
    def visit_FunctionReturn(self, node):
        value = self.visit(node.value_node)
        self.stack.push(value)
    
    def visit_Number(self, node):
        return BasicValue(node.value)
    
    def visit_String(self, node):
        return BasicValue(node.value)
    
    def visit_UnaryOp(self, node):
        val = self.visit(node.expression)
        
        if node.token.type == TokenType.Plus:
            return BasicValue(+val.value)
        elif node.token.type == TokenType.Minus:
            return BasicValue(-val.value)
            
        elif node.token.type == TokenType.Not:
            if val is None or val.value == 0:
                return BasicValue(1)
            else:
                return BasicValue(0)
            
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

    def assignment_typecheck(self, node, type_object, assignment_value):
        if type_object is None:
            self.error(node.lhs, ErrorType.TypeError, 'Set with decltype but decltype resolved to None')
            return False
        elif not isinstance(type_object, BasicType):
            self.error(node.lhs, ErrorType.TypeError, '{} is not a valid type object and cannot be used as a declaration type'.format(type_object))
            return False
        else:
            assignment_type = BasicValue(assignment_value).lookup_type(self.global_scope)

            if isinstance(assignment_type, BasicObject):
                assignment_type = assignment_value.parent

            if assignment_type is None:
                self.error(node.value, ErrorType.TypeError, 'Assignment requires type {} but could not resolve a runtime type of assignment value'.format(type_object))
                return None
            if isinstance(assignment_type, BasicValue):
                assignment_type = assignment_type.extract_value()

            if not isinstance(assignment_type, BasicType):
                self.error(node.value, ErrorType.TypeError, '{} is not a valid runtime type object'.format(assignment_type))
                return False
    
            if not type_object.compare_type(assignment_type):
                self.error(node.value, ErrorType.TypeError, 'Attempted to assign <{}> to a value of type <{}>'.format(type_object.friendly_typename, assignment_type.friendly_typename))
                return False

        return True

    def visit_Assign(self, node):
        if node.value.type == NodeType.FunctionExpression:
            value = node.value
        else:
            value = self.visit(node.value)

        if isinstance(node.lhs, NodeVariable):
            target_info = self.walk_variable(node.lhs)
            target_value = target_info.value_wrapper

            # TYPE CHECK
            if target_info.decltype is not None:
                typecheck_value = self.assignment_typecheck(node, target_info.decltype, value)

                if typecheck_value is not True:
                    return None

            target_value.assign_value(value)

        elif isinstance(node.lhs, NodeMemberExpression):
            (target, member) = self.walk_member_expression(node.lhs)

            if not isinstance(target, BasicObject):
                self.error(node, ErrorType.TypeError, 'member expression not assignable')
                return None

            target_type = target.parent

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
        return_value = 0 # TODO make Null-ish type -- "Unset" type ?
        # TODO make it an error if you declare the type function should return and no value provided

        if target is None:
            target = self.visit(node.lhs) # TODO: turn into general expression, not just vars.

        if target is not None:
            this_value = None
            is_member_call = False

            # for `a.b()`, pass in `a` as the this value.
            if isinstance(node.lhs, NodeMemberExpression):
                is_member_call = True
                this_value = self.visit(node.lhs.lhs)

            # if a built-in function exists, call it
            if isinstance(target, BuiltinFunction):
                return self.call_builtin_function(target, this_value, node.argument_list.arguments, node)
                
            # user-defined function
            elif isinstance(target, NodeFunctionExpression):
                expected_arg_count = len(target.argument_list.arguments)
                given_arg_count = len(node.argument_list.arguments)

                if is_member_call: # a.b('test') -> pass 'a' in as first argument
                    self.stack.push(this_value)

                    given_arg_count += 1

                if expected_arg_count != given_arg_count:
                    self.error(node, ErrorType.ArgumentError, 'method expected {} arguments, {} given'.format(expected_arg_count, given_arg_count))
                    return None

                #TODO assert argument size is declared arg size - 1
                
                # push arguments to stack
                for arg in node.argument_list.arguments:
                    self.stack.push(self.visit(arg))

                
                self.call_function_expression(target)
                # the return value is pushed onto the stack at end of block or return
                # statement. Pop it off and return as a value

                return self.stack.pop()

        self.error(node, ErrorType.TypeError, 'invalid call: {} is not callable'.format(target))

    def walk_variable(self, node):
        var = self.current_scope.find_variable_info(node.value)

        if var is None:
            self.error(node, ErrorType.DoesNotExist, "Referencing undefined variable '{}'".format(node.value))
            return None

        return var
            
    def visit_Variable(self, node):
        var = self.walk_variable(node)

        if var is not None:
            return var.value_wrapper.value

        return None
        
    def visit_IfStatement(self, node):
        expr_result = self.visit(node.expr)

        # todo this should be changed to a general purpose 'is true' check
        if expr_result.truthy:
            return self.visit_Block(node.block)
        elif node.else_block is not None:
            # use visit rather than direct to visit_Block
            # since else_block can also be a NodeIfStatement in the
            # case of `elif`
            return self.visit(node.else_block)
            
    def visit_While(self, node):
        expr_result = self.visit(node.expr)
        
        if expr_result.truthy:
            self.visit(node.block)
            self.visit_While(node)
        
    def visit_ArgumentList(self, node):
        # read arguments backwards as values are popped from stack
        for argument in reversed(node.arguments):
            # retrieve value
            value = self.stack.pop()
            # declare variable
            self.visit_Declare(argument)
            # TODO: clean up
            # set variable to passed in value
            if isinstance(value, AstNode):
                value = self.visit(value)

            self.current_scope.set_variable(argument.name.value, value)

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
        last_child = None
        for child in node.block.children:
            last_child = child
            if type(child) == NodeFunctionReturn:
                break

        # no return statement, push return code 0 to the stack
        #print("last_child = {}".format(last_child))
        if type(last_child) != NodeFunctionReturn:
            self.stack.push(0)
            
        # done, close scope
        self.close_scope()

    def visit_ArrayExpression(self, node):
        members = []

        for member_decl in node.members:
            value = self.visit(member_decl)

            members.append(value)

        return BasicValue(members)

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

    def basic_value_to_object(self, node, target):
        target = BasicValue(target).extract_basicvalue()

        if not isinstance(target, BasicObject):
            target_type_object = target.lookup_type(self.global_scope).extract_basicvalue()

            if target_type_object is None:
                self.error(node, ErrorType.TypeError, 'invalid member access: target {} is not a BasicObject'.format(target))
                return None

            # for a string this would basically mean:
            # "hello ".append("world")
            # -> Str.new("hello ").append("world")
            target = builtin_object_new([self, target_type_object, target])

        return target

    def walk_member_expression(self, node):
        target = self.visit(node.lhs)

        if target is None:
            self.error(node, ErrorType.TypeError, 'invalid member access: {} has no member {}'.format(target, node.identifier))
            return None

        target = self.basic_value_to_object(node, target)

        member = target.lookup_member(node.identifier.value)

        if member is None:
            self.error(node, ErrorType.TypeError, 'object {} has no direct or inherited member `{}`'.format(target, node.identifier.value))

        return (target, member)

    def visit_MemberExpression(self, node):
        return self.walk_member_expression(node)[1].value

    def visit_ArrayAccessExpression(self, node):
        member_access_call_node = NodeCall(
            NodeMemberExpression(
                node.lhs,
                LexerToken('__at__', TokenType.Identifier),
                node.token
            ),
            NodeArgumentList(
                [node.access_expr],
                node.token
            )
        )

        return self.visit(member_access_call_node)
        
    def visit_Empty(self, node):
        pass
    
