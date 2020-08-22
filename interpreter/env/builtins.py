from interpreter.typing.basic_type import BasicType
from interpreter.basic_object import BasicObject
from interpreter.basic_value import BasicValue
from interpreter.function import BuiltinFunction
from parser.node import NodeFunctionExpression
from error import ErrorType

def _print_object(interpreter, node, obj):
    obj_str = str(obj)

    if isinstance(obj, BasicObject):
        meth = obj.lookup_member(BasicType.REPR_FUNCTION_NAME)

        basic_value_repr = None

        if meth is not None:
            if isinstance(meth.value, BuiltinFunction):
                basic_value_repr = interpreter.call_builtin_function(meth.value, obj, [], node)
            else:
                basic_value_repr = interpreter.call_function_expression(meth.value)

            if not isinstance(basic_value_repr, BasicValue):
                interpreter.error(node, ErrorType.TypeError, 'expected {} method to return an instance of BasicValue, got {}'.format(BasicType.REPR_FUNCTION_NAME, basic_value_repr))
                return None

            obj_str = basic_value_repr.value

    print(obj_str)
    
def builtin_varinfo(arguments):
    interpreter = arguments[0]
    var = interpreter.current_scope.find_variable_info(arguments[2])

    #varinfo_str = f"Variable '{arguments[2]}'\n\t" \
    #    f"decltype: {var.decltype}\n\t" \
    #    f"value: {var.value_wrapper}\n\t" \
    #    f"runtime type: {var.value_wrapper.lookup_type(interpreter.global_scope)}\n"
        
    varinfo_str = \
    f"""Variable '{arguments[2]}'
    decltype: {var.decltype}
    value: {var.value_wrapper}
    runtime type: {var.value_wrapper.lookup_type(interpreter.global_scope)}
    """

    return BasicValue(varinfo_str)

def builtin_printn(arguments):
    interpreter = arguments[0]
    node = arguments[1]

    for arg in arguments[2:]:
        _print_object(interpreter, node, arg)

    return BasicValue(None)

def builtin_exit(arguments):
    interpreter = arguments[0]
    node        = arguments[1]
    return_code = arguments[2]
    
    exit(return_code)
    
    return BasicValue(0)

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
        return BasicValue(1)
    else:
        return BasicValue(0)

# PLACEHOLDER
def builtin_to_int(arguments):
    return BasicValue(int(arguments[1].value))

def builtin_str_len(arguments):
    return BasicValue(len(arguments[1].value))

def builtin_object_new(arguments):
    interpreter = arguments[0]
    this_object = arguments[1]

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
            interpreter.call_builtin_function(constructor_method, this_object, arguments[2:-1], None)
        elif isinstance(constructor_method, NodeFunctionExpression):
            # push this object + any arguments passed here to the function
            interpreter.stack.push(new_instance)

            sliced = arguments[2:-1]

            for i in range(0, len(constructor_method.argument_list.arguments) - 1):
                if i >= len(sliced):
                    interpreter.stack.push(BasicValue(None))
                else:
                    interpreter.stack.push(sliced[i])


            interpreter.call_function_expression(constructor_method)
        else:
            interpreter.error(None, ErrorType.TypeError, 'invalid constructor type {}'.format(constructor_method))

    return new_instance

def builtin_object_type(arguments):
    interpreter = arguments[0]
    this_object = arguments[1]

    if not isinstance(this_object, BasicValue):
        interpreter.error(None, ErrorType.TypeError, 'object {} is not an instance of BasicValue'.format(this_object))
        return None

    return this_object.lookup_type(interpreter.global_scope)

def builtin_object_to_str(arguments):
    interpreter = arguments[0]
    this_object = arguments[1]

    return BasicValue('Object')

def builtin_value_to_str(arguments):
    interpreter = arguments[0]
    this_object = arguments[1]

    value_member = this_object.lookup_member('_value')

    if value_member is None:
        interpreter.error(None, ErrorType.TypeError, '_value is not a member of {}'.format(this_object))
        return None

    return BasicValue(str(value_member.value))

def builtin_num_to_str(arguments):
    return builtin_value_to_str(arguments)

def builtin_str_to_str(arguments):
    return builtin_value_to_str(arguments)

def builtin_type_extend(arguments):
    interpreter = arguments[0]
    this_object = arguments[1]

    if len(arguments) > 2:
        provided_args = arguments[2]

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
    interpreter = arguments[0]
    this_object = arguments[1]

    if this_object.parent is not None:
        return this_object.parent

    return this_object.lookup_type(interpreter.global_scope)

def builtin_type_to_str(arguments):
    interpreter = arguments[0]
    this_object = arguments[1]

    return BasicValue(repr(this_object))
