from interpreter.typing.basic_type import BasicType
from interpreter.basic_object import BasicObject
from interpreter.variable import VariableType
from interpreter.basic_value import BasicValue
from interpreter.function import BuiltinFunction
from interpreter.env.builtins import *

class Globals:
    def __init__(self):
        self.basic_type = BasicType(
            None,
            {
                'name': BasicValue('Type'),
                'extend': BuiltinFunction('Type.extend', None, builtin_type_extend),
                # 'type': BuiltinFunction('Type.type', None, builtin_type_type),
                'to_str': BuiltinFunction('Type.to_str', None, builtin_type_to_str),
                # 'new': BuiltinFunction('Object.new', None, builtin_object_new),
            },
            True
        )
        self.basic_object = BasicType(
            self.basic_type,
            {
                'instance': BasicObject(members={}),
                'name': BasicValue('Object'),
                'new': BuiltinFunction('Object.new', None, builtin_object_new),
                'type': BuiltinFunction('Object.type', None, builtin_object_type),
                'to_str': BuiltinFunction('Object.to_str', None, builtin_object_to_str)
            }
        )

        self.basic_type.parent = self.basic_object # circular

        self.basic_number = BasicType(
            self.basic_object,
            {
                'name': BasicValue('Num'),
                'to_int': BuiltinFunction('Num.to_int', None, builtin_to_int),
                'to_str': BuiltinFunction('Num.to_str', None, builtin_num_to_str)
            }
        )

        self.func_type = BasicType(
            self.basic_object,
            {
                'name': BasicValue('Func')
                # TODO call function
            }
        )

        self.int_type = BasicType(
            self.basic_number,
            {
                'name': BasicValue('Int'),
                'instance': BasicObject(members={
                    '_value': BasicValue(value=0)
                }),
            }
        )

        # self.float_type = BasicType(
        #     self.basic_number,
        #     {
        #         'name': BasicValue('Float'),
        #         'instance': BasicObject(members={
        #             '_value': BasicValue(value=0.0)
        #         })
        #     }
        # )

        self.str_type = BasicType(
            self.basic_object,
            {
                'name': BasicValue('Str'),
                'instance': BasicObject(members={
                    '_value': BasicValue(value="")
                }),
                'len': BuiltinFunction('Str.len', None, builtin_str_len),
                'to_str': BuiltinFunction('Str.to_str', None, builtin_str_to_str)
            }
        )

        self.variables = [
            ('Type', VariableType.Object, self.basic_type),
            ('Object', VariableType.Type, self.basic_object),
            ('Func', VariableType.Type, self.func_type),
            ('Num', VariableType.Type, self.basic_number),
            (
                'Int',
                VariableType.Type,
                self.int_type
            ),
            # (
            #     'Float',
            #     VariableType.Type,
            #     self.float_type
            # ),
            (
                'Str',
                VariableType.Type,
                self.str_type
            ),
            ('__intern_print__', VariableType.Function, BuiltinFunction("__intern_print__", None, builtin_printn)),
            ('__intern_type_compare__', VariableType.Function, BuiltinFunction("__intern_type_compare__", None, builtin_type_compare)),
            ('__intern_varinfo__', VariableType.Function, BuiltinFunction("__intern_varinfo__", None, builtin_varinfo)),
            ('__intern_exit__', VariableType.Function, BuiltinFunction("__intern_exit__", None, builtin_exit)),
            ('__intern_console_input__', VariableType.Function, BuiltinFunction("__intern_console_input__", None, builtin_console_input)),
            ('__intern_file_read__', VariableType.Function, BuiltinFunction("__intern_file_read__", None, builtin_file_read)),
            ('__intern_file_write__', VariableType.Function, BuiltinFunction("__intern_file_write__", None, builtin_file_write))
        ]

    def vartype_to_typeobject(self, vartype):
        if vartype == VariableType.Int:
            return self.int_type
        # elif vartype == VariableType.Float
        elif vartype == VariableType.String:
            return self.str_type
        elif vartype == VariableType.Function:
            return self.func_type
        elif vartype == VariableType.Type:
            return self.basic_type
        elif vartype == VariableType.Object:
            return self.basic_object

        raise Exception('No conversion defined for {}'.format(vartype))

    def apply_to_scope(self, scope):
        for (name, vtype, value) in self.variables:
            var_type = vtype

            type_object = self.vartype_to_typeobject(var_type)

            scope.declare_variable(name, type_object)

            var = scope.find_variable_value(name)
            var.assign_value(value)

        #print(scope)
