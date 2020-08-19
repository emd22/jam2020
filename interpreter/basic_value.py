class BasicValue:
    def __init__(self, value):
        self.assign_value(value)

    def assign_value(self, value):
        self.value = value

    def lookup_type(self, global_scope):
        if type(self.value) is str:
            return global_scope.find_variable_value('Str')
        elif type(self.value) is int:
            return global_scope.find_variable_value('Int')
        elif type(self.value) is float:
            return global_scope.find_variable_value('Float')
        # function, builtinfunction, etc.
        else:
            return global_scope.find_variable_value('Object')

    def clone(self):
        return BasicValue(self.value)

    def __repr__(self):
        return repr(self.value)
        # return "BasicValue({})".format(repr(self.value))