from interpreter.typing.basic_type import BasicType
from interpreter.basic_object import BasicObject
from interpreter.scope import VariableType
from interpreter.variable import Value
from interpreter.function import BuiltinFunction
from error import ErrorType

# PLACEHOLDER
def builtin_to_int(arguments):
    print("to_int called with arugments {}".format(arguments))

    return Value(int(arguments[1].value))

def builtin_str_len(arguments):
    return Value(len(arguments[1].value))

def builtin_object_new(arguments):
    interpreter = arguments[0]
    this_object = arguments[1]

    new_instance = None

    if 'instance' in this_object.members and isinstance(this_object.members['instance'], BasicObject):
        new_instance = this_object.members['instance'].clone(parent_override=this_object)
    else:
        interpreter.error(None, ErrorType.TypeError, 'object {} cannot be constructed because no cloneable `instance` member exists'.format(this_object))
        return None

    return new_instance

class Globals:
    def __init__(self):
        basic_type = BasicType('Type', None, {}, True)
        basic_object = BasicType(
            'Object',
            basic_type,
            {
                'instance': BasicObject(members={}),
                'name': 'Object',
                'new': BuiltinFunction('Object.new', None, builtin_object_new),
                'type': BuiltinFunction('Object.type', None, builtin_object_type),
                'to_str': BuiltinFunction('Object.to_str', None, builtin_object_to_str)
            }
        )
        basic_number = BasicType(
            'Num',
            basic_object,
            {
                'to_int': BuiltinFunction('__intern_to_int__', None, builtin_to_int)
            }
        )

        basic_function = BasicType(
            basic_object,
            {
                'name': 'Func'
                # TODO call function
            }
        )

        self.variables = [
            ('Type', VariableType.Object, basic_type),
            ('Object', VariableType.Type, basic_object),
            ('Func', VariableType.Type, basic_function),
            ('Num', VariableType.Type, basic_number),
            (
                'Int',
                VariableType.Type,
                BasicType(
                    'Int',
                    basic_number,
                    {
                        'instance': BasicObject(members={
                            '_value': Value(value=0)
                        }),
                    }
                )
            ),
            (
                'Float',
                VariableType.Type,
                BasicType(
                    'Float',
                    basic_number,
                    {
                        'instance': BasicObject(members={
                            '_value': Value(value=0.0)
                        })
                    }
                )
            ),
            (
                'Str',
                VariableType.Type,
                BasicType(
                    'Str',
                    basic_object,
                    {
                        'instance': BasicObject(members={
                            '_value': Value(value="")
                        }),
                        'len': BuiltinFunction('__intern_str_len__', None, builtin_str_len)
                    }
                )
            )
        ]

    def apply_to_scope(self, scope):
        for (name, vtype, value) in self.variables:
            var_type = vtype

            scope.declare_variable(name, var_type)

            var = scope.find_variable(name)
            var.assign_value(value)