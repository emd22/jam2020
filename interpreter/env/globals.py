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

        self.func_type = BasicType(
            self.basic_type,
            {
                'name': BasicValue('Func'),
                'instance': BasicObject(members={})
            }
        )

        self.variables = [
            ('Type', VariableType.Object, self.basic_type),
            ('Object', VariableType.Type, self.basic_object),
            ('Func', VariableType.Type, self.func_type),
            ('__intern_object_patch__', VariableType.Function, BuiltinFunction("__intern_object_patch__", None, builtin_object_patch)),
            ('__intern_print__', VariableType.Function, BuiltinFunction("__intern_print__", None, builtin_printn)),
            ('__intern_type_compare__', VariableType.Function, BuiltinFunction("__intern_type_compare__", None, builtin_type_compare)),
            ('__intern_varinfo__', VariableType.Function, BuiltinFunction("__intern_varinfo__", None, builtin_varinfo)),
            ('__intern_exit__', VariableType.Function, BuiltinFunction("__intern_exit__", None, builtin_exit)),
            ('__intern_to_int__', VariableType.Function, BuiltinFunction("__intern_to_int__", None, builtin_to_int)),
            ('__intern_num_to_str__', VariableType.Function, BuiltinFunction("__intern_num_to_str__", None, builtin_num_to_str)),
            ('__intern_str_len__', VariableType.Function, BuiltinFunction("__intern_str_len__", None, builtin_str_len)),
            ('__intern_str_append__', VariableType.Function, BuiltinFunction("__intern_str_append__", None, builtin_str_append)),
            ('__intern_array_len__', VariableType.Function, BuiltinFunction("__intern_array_len__", None, builtin_array_len)),
            ('__intern_array_at__', VariableType.Function, BuiltinFunction("__intern_array_at__", None, builtin_array_at)),
            ('__intern_console_input__', VariableType.Function, BuiltinFunction("__intern_console_input__", None, builtin_console_input)),
            ('__intern_file_read__', VariableType.Function, BuiltinFunction("__intern_file_read__", None, builtin_file_read)),
            ('__intern_file_write__', VariableType.Function, BuiltinFunction("__intern_file_write__", None, builtin_file_write)),

            ('__intern_int_add__', VariableType.Function, BuiltinFunction("__intern_int_add__", None, builtin_int_add)),
            ('__intern_int_sub__', VariableType.Function, BuiltinFunction("__intern_int_sub__", None, builtin_int_sub)),
            ('__intern_int_mul__', VariableType.Function, BuiltinFunction("__intern_int_mul__", None, builtin_int_mul)),
            ('__intern_int_div__', VariableType.Function, BuiltinFunction("__intern_int_div__", None, builtin_int_div)),
        ]

    def vartype_to_typeobject(self, vartype):
        if vartype == VariableType.Function:
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
