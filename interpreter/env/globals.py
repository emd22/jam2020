from interpreter.typing.basic_type import BasicType
from interpreter.basic_object import BasicObject
from interpreter.variable import VariableType
from interpreter.basic_value import BasicValue
from interpreter.function import BuiltinFunction
from interpreter.env.builtins import *

class Globals:
    def __init__(self):
        basic_type = BasicType(
            None,
            {
                'name': 'Type',
                'extend': BuiltinFunction('Type.extend', None, builtin_type_extend),
                # 'type': BuiltinFunction('Type.type', None, builtin_type_type),
                'to_str': BuiltinFunction('Type.to_str', None, builtin_type_to_str),
                # 'new': BuiltinFunction('Object.new', None, builtin_object_new),
            },
            True
        )
        basic_object = BasicType(
            basic_type,
            {
                'instance': BasicObject(members={}),
                'name': 'Object',
                'new': BuiltinFunction('Object.new', None, builtin_object_new),
                'type': BuiltinFunction('Object.type', None, builtin_object_type),
                'to_str': BuiltinFunction('Object.to_str', None, builtin_object_to_str)
            }
        )

        basic_type.parent = basic_object # circular

        basic_number = BasicType(
            basic_object,
            {
                'name': 'Num',
                'to_int': BuiltinFunction('Num.to_int', None, builtin_to_int),
                'to_str': BuiltinFunction('Num.to_str', None, builtin_num_to_str)
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
                    basic_number,
                    {
                        'name': 'Int',
                        'instance': BasicObject(members={
                            '_value': BasicValue(value=0)
                        }),
                    }
                )
            ),
            (
                'Float',
                VariableType.Type,
                BasicType(
                    basic_number,
                    {
                        'name': 'Float',
                        'instance': BasicObject(members={
                            '_value': BasicValue(value=0.0)
                        })
                    }
                )
            ),
            (
                'Str',
                VariableType.Type,
                BasicType(
                    basic_object,
                    {
                        'name': 'Str',
                        'instance': BasicObject(members={
                            '_value': BasicValue(value="")
                        }),
                        'len': BuiltinFunction('Str.len', None, builtin_str_len),
                        'to_str': BuiltinFunction('Str.to_str', None, builtin_str_to_str)
                    }
                )
            ),
            ('__intern_print__', VariableType.Function, BuiltinFunction("__intern_print__", None, builtin_printn)),
            ('__intern_type_compare__', VariableType.Function, BuiltinFunction("__intern_type_compare__", None, builtin_type_compare)),
            ('__intern_varinfo__', VariableType.Function, BuiltinFunction("__intern_varinfo__", None, builtin_varinfo)),
            ('__intern_exit__', VariableType.Function, BuiltinFunction("__intern_exit__", None, builtin_exit)),
        ]

    def apply_to_scope(self, scope):
        for (name, vtype, value) in self.variables:
            var_type = vtype

            scope.declare_variable(name, var_type)

            var = scope.find_variable_value(name)
            var.assign_value(value)

        print(scope)
