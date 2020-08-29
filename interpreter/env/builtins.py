from interpreter.typing.basic_type import BasicType
from interpreter.basic_object import BasicObject
from interpreter.basic_value import BasicValue
from interpreter.function import BuiltinFunction
from interpreter.env.builtin.arith import *
from interpreter.env.builtin.time import *
from parser.node import NodeFunctionExpression, NodeCall, NodeArgumentList, NodeMemberExpression, NodeNone
from error import ErrorType
from util import LogColour

def obj_to_string(interpreter, node, obj):
    obj_str = str(obj)

    obj = interpreter.basic_value_to_object(node, obj)

    if isinstance(obj, BasicObject):
        meth = obj.lookup_member(BasicType.REPR_FUNCTION_NAME)

        basic_value_repr = None

        if meth is not None:
            if isinstance(meth.value, BuiltinFunction):
                basic_value_repr = interpreter.call_builtin_function(meth.value, obj, [], node)
            else:
                interpreter.stack.push(obj)
                interpreter.call_function_expression(meth.value)
                basic_value_repr = interpreter.stack.pop()

            if not isinstance(basic_value_repr, BasicValue):
                interpreter.error(node, ErrorType.TypeError, 'expected {} method to return an instance of BasicValue, got {}'.format(BasicType.REPR_FUNCTION_NAME, basic_value_repr))
                return None

            obj_str = basic_value_repr.value

    return obj_str

def _print_object(interpreter, node, obj, end='\n'):
    print(obj_to_string(interpreter, node, obj), end=end)
    
def builtin_varinfo(arguments):
    interpreter = arguments.interpreter
    var = interpreter.current_scope.find_variable_info(arguments.arguments[0].value)

    if var == None:
        return BasicValue("")

    varinfo_str = f"Variable '{arguments.arguments[0]}'\n\t" \
        f"decltype: {var.decltype}\n\t" \
        f"value: {var.value_wrapper}\n\t" \
        f"runtime type: {var.value_wrapper.lookup_type(interpreter.global_scope)}\n"
    

    return BasicValue(varinfo_str)

def builtin_console_write(arguments):
    interpreter = arguments.interpreter
    node = arguments.node

    for arg in arguments.arguments:
        _print_object(interpreter, node, arg, end='')

    return BasicValue(len(arguments.arguments))

def builtin_printn(arguments):
    interpreter = arguments.interpreter
    node = arguments.node

    for arg in arguments.arguments:
        _print_object(interpreter, node, arg)

    return BasicValue(len(arguments.arguments))

def builtin_print_color(arguments):
    color = arguments.arguments[0].extract_value()
    if color == 0:
        print(f"{LogColour.Default}", end="")
    elif color == 1:
        print(f"{LogColour.Error}", end="")
    elif color == 2:
        print(f"{LogColour.Warning}", end="")
    elif color == 3:
        print(f"{LogColour.Info}", end="")
    elif color == 4:
        print(f"{LogColour.Bold}", end="")
    return BasicValue(0)
    

def builtin_exit(arguments):
    interpreter = arguments.interpreter
    node        = arguments.node
    return_code = arguments.arguments[0]
    
    exit(return_code)
    
    return BasicValue(0)

def builtin_type_compare(arguments):
    interpreter = arguments.interpreter
    node = arguments.node
    target = arguments.arguments[0]
    type_obj = arguments.arguments[1]

    if not isinstance(target, BasicObject):
        interpreter.error(node, ErrorType.TypeError, 'argument 1 ({}) is not a BasicObject, cannot perform typecheck'.format(target))
        return None

    if not isinstance(type_obj, BasicType):
        interpreter.error(node, ErrorType.TypeError, 'argument 2 ({}) is not a BasicType, cannot perform typecheck'.format(type_obj))

    if target.satisfies_type(type_obj):
        return BasicValue(1)
    else:
        return BasicValue(0)

# simple == compare
def builtin_default_compare(arguments):
    interpreter = arguments.interpreter
    node = arguments.node
    target = arguments.arguments[0].extract_value()
    other = arguments.arguments[1].extract_value()

    return BasicValue(int(target == other))

def builtin_int_negate(arguments):
    interpreter = arguments.interpreter
    node = arguments.node
    target = arguments.arguments[0].extract_value()

    return BasicValue(int(not target))

def builtin_to_int(arguments):
    return BasicValue(int(arguments.arguments[0].extract_value()))

def builtin_to_float(arguments):
    return BasicValue(float(arguments.arguments[0].extract_value()))

def builtin_str_len(arguments):
    return BasicValue(len(str(arguments.arguments[0].extract_value())))

def builtin_array_len(arguments):
    return BasicValue(len(arguments.arguments[0].extract_value()))

def builtin_array_set(arguments):
    array = arguments.arguments[0].extract_value()
    index = arguments.arguments[1].extract_value()
    value = arguments.arguments[2].extract_value()

    array[index] = value

    return BasicValue(array)

def builtin_array_clone(arguments):
    array = arguments.arguments[0].extract_value()
    new_array = array.copy()
    return BasicValue(new_array)

def builtin_array_at(arguments):
    obj = arguments.arguments[0].extract_value()
    index = arguments.arguments[1].extract_value()

    if index > len(obj):
        # TODO make throw internal exception
        return BasicValue(None)

    return BasicValue(obj[index])
    
def builtin_array_append(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    
    value_start = arguments.arguments[0]
    
    value = value_start.extract_value()

    if len(arguments.arguments) > 1:
        for arg in arguments.arguments[1:]:
            value.append(arg.extract_value())

    return BasicValue(value)

def builtin_str_append(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    str_value_start = arguments.arguments[0]

    str_value = str(str_value_start.extract_value())

    if len(arguments.arguments) > 1:
        for arg in arguments.arguments[1:]:
            str_value = str_value + str(arg.extract_value())

    return BasicValue(str_value)

def builtin_object_new(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    node = arguments.node

    new_instance = None

    if 'instance' in this_object.members and isinstance(this_object.members['instance'], BasicObject):
        new_instance = this_object.members['instance'].clone(parent_override=this_object)
    else:
        interpreter.error(None, ErrorType.TypeError, 'object {} cannot be constructed because no cloneable `instance` member exists'.format(this_object))
        return None

    # if there is a constructor function, call that...
    constructor_method_member = this_object.lookup_member('__construct__')

    if constructor_method_member is not None:
        constructor_method = constructor_method_member.value

        if isinstance(constructor_method, BuiltinFunction):
            interpreter.call_builtin_function(constructor_method, this_object, arguments.arguments, None)
        elif isinstance(constructor_method, NodeFunctionExpression):
            # push this object + any arguments passed here to the function
            passed_args = [new_instance, *arguments.arguments]

            for i in range(0, len(constructor_method.argument_list.arguments)):
                if i >= len(passed_args):
                    interpreter.stack.push(BasicValue(None))
                else:
                    interpreter.stack.push(passed_args[i])

            interpreter.call_function_expression(constructor_method)

            # pop return value off stack - if no `return X` is given,
            # a default value is pushed to stack anyway.
            interpreter.stack.pop()
        else:
            interpreter.error(None, ErrorType.TypeError, 'invalid constructor type {}'.format(constructor_method))

    return new_instance

def builtin_object_type(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    if not isinstance(this_object, BasicValue):
        interpreter.error(None, ErrorType.TypeError, 'object {} is not an instance of BasicValue'.format(this_object))
        return None

    return this_object.lookup_type(interpreter.global_scope)

def builtin_object_to_str(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    return BasicValue('Object')

def builtin_object_patch(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    target = arguments.arguments[0].extract_value()
    patch = arguments.arguments[1].extract_value()

    if not isinstance(target, BasicObject):
        interpreter.error(this_object, ErrorType.TypeError, 'Cannot patch non-BasicObject value: {}'.format(target))
        return None

    if not isinstance(target, BasicObject):
        interpreter.error(this_object, ErrorType.TypeError, 'Cannot patch object with non-BasicObject value: {}'.format(patch))
        return None

    for (member_name, member_value) in patch.members.items():
        target.assign_member(member_name, member_value)

    return target

def builtin_value_to_str(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    
    passed_arg = arguments.arguments[0].extract_value()

    return BasicValue(str(passed_arg))

def builtin_num_to_str(arguments):
    return builtin_value_to_str(arguments)

def builtin_str_to_str(arguments):
    return builtin_value_to_str(arguments)

def builtin_type_extend(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    if len(arguments.arguments) > 0:
        provided_args = arguments.arguments[0]

        if not isinstance(provided_args, BasicObject):
            interpreter.error('provided args to Type.extend must be an instance of BasicObject, got {}'.format(provided_args))
            return None

        extended_properties = provided_args.members
    else:
        extended_properties = {}

    instance_members = {}

    if 'instance' in this_object.members:
        instance_members = this_object.members['instance'].clone().members
        #for (member_name, member_value) in this_object.members['instance'].members.items():
         #instance_members[member_name] = member_value.clone()

    instance_members.update(extended_properties)

    return BasicType(this_object, instance_members)

def builtin_type_type(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    if this_object.parent is not None:
        return this_object.parent

    return this_object.lookup_type(interpreter.global_scope)

def builtin_type_to_str(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    return BasicValue(repr(this_object))

def builtin_console_input(arguments):
    input_result = input()

    return BasicValue(input_result)

def builtin_file_read(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    file_path = arguments.arguments[0]

    # TODO better exception handling - throw internal exception
    try:
        f = open(file_path.extract_value(), 'r')
        s = f.read()
    except:
        s = ""

    return BasicValue(s)

def builtin_file_write(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object

    file_path = arguments.arguments[0]
    write_value = arguments.arguments[1]

    f = open(file_path.extract_value(), 'w')
    f.write(str(write_value.extract_value()))
    f.close()

    return BasicValue(file_path)

def builtin_func_call(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    node = arguments.node

    meth = arguments.arguments[0]
    arg_array = arguments.arguments[1].extract_value()

    if not isinstance(arg_array, list):
        interpreter.error(node, ErrorType.TypeError, '__intern_func_call__ expects arguments to be passed as an array but got {}'.format(arg_array))
        return None

    if isinstance(meth, BuiltinFunction):
        basic_value_resp = interpreter.call_builtin_function(meth, this_object, arg_array, node)
    else:
        for arg in arg_array:
            interpreter.stack.push(arg)
        interpreter.call_function_expression(meth)
        basic_value_resp = interpreter.stack.pop()

    return basic_value_resp

def builtin_math_max(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    node = arguments.node

    values = []

    for arg in arguments.arguments:
        v = arg.extract_value()
        values.append(v)

    max_value = max(values)

    return BasicValue(max_value)

def builtin_math_min(arguments):
    interpreter = arguments.interpreter
    this_object = arguments.this_object
    node = arguments.node

    values = []

    for arg in arguments.arguments:
        v = arg.extract_value()
        values.append(v)

    min_value = min(values)

    return BasicValue(min_value)

def builtin_macro_expand(arguments):
    from lexer import Lexer
    from parser.parser import Parser

    interpreter = arguments.interpreter
    this_object = arguments.this_object
    src_data = arguments.arguments[0].extract_value()

    if not isinstance(src_data, str):
        interpreter.error(arguments.node, ErrorType.TypeError, 'Expected a string for macro expansion')
        return None

    lexer = Lexer(src_data, interpreter.source_location)
    tokens = lexer.lex()

    parser = Parser(tokens, lexer.source_location)
    
    ast = parser.parse()

    if len(parser.error_list.errors) > 0:
        interpreter.error(arguments.node, ErrorType.MacroExpansionError, 'Macro expansion failed:\n{}'.format('\t'.join(map(lambda x: str(x), parser.error_list.errors))))
        return None

    for node in ast:
        interpreter.visit(node)

    return BasicValue(None)
