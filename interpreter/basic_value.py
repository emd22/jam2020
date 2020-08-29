from parser.node import NodeFunctionExpression, NodeMacro
from interpreter.function import BuiltinFunction

class BasicValue:
    def __init__(self, value):
        self.assign_value(value)

    def compare_value(self, other):
        return self.extract_value() == other.extract_value()

    def assign_value(self, value):
        self.value = value

    def extract_basicvalue(self):
        if self.value is not None and isinstance(self.value, BasicValue):
            return self.value.extract_basicvalue()

        return self

    def extract_value(self):
        if isinstance(self.value, BasicValue):
            return self.value.extract_value()

        return self.value

    def lookup_type(self, global_scope):
        from interpreter.basic_object import BasicObject

        if isinstance(self.value, BasicValue):#type(self.value) == BasicValue:
            return self.value.lookup_type(global_scope)
        elif isinstance(self.value, NodeFunctionExpression) or isinstance(self.value, BuiltinFunction):
            return global_scope.find_variable_value('Func')
        elif isinstance(self.value, NodeMacro):
            return global_scope.find_variable_value('Macro')
        elif type(self.value) is str:
            return global_scope.find_variable_value('Str')
        elif type(self.value) is int:
            return global_scope.find_variable_value('Int')
        elif type(self.value) is float:
            return global_scope.find_variable_value('Float')
        elif type(self.value) is list:
            return global_scope.find_variable_value('Array')
        elif type(self.value) is bool:
            return global_scope.find_variable_value('Bool')
        elif self.value is None:
            return global_scope.find_variable_value('Null')
        else:
            raise Exception('could not get type for {}'.format(self))

    def clone(self):
        return BasicValue(self.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)
        
