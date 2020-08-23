from parser.node import NodeFunctionExpression

class BasicValue:
    def __init__(self, value):
        self.assign_value(value)

    def assign_value(self, value):
        self.value = value

    def extract_value(self):
        if isinstance(self.value, BasicValue):#type(self.value) == BasicValue:
            return self.value.extract_value()

        return self.value

    def lookup_type(self, global_scope):
        from interpreter.basic_object import BasicObject

        if isinstance(self.value, BasicValue):#type(self.value) == BasicValue:
            return self.value.lookup_type(global_scope)
        elif isinstance(self.value, NodeFunctionExpression):
            return global_scope.find_variable_value('Func')
        elif type(self.value) is str:
            return global_scope.find_variable_value('Str')
        elif type(self.value) is int:
            return global_scope.find_variable_value('Int')
        elif type(self.value) is float:
            return global_scope.find_variable_value('Float')
        # elif isinstance(self.value, BasicObject):
            # print("self.value.parent is {}".format(self.value.parent))
            # if self.value.parent is not None:
            #     return self.value.parent
            # else:
            #     return global_scope.find_variable_value('Object')
        else:
            return global_scope.find_variable_value('Any')

    def clone(self):
        return BasicValue(self.value)

    def __repr__(self):
        return repr(self.value)
        # return "BasicValue({})".format(repr(self.value))