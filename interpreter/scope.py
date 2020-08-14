from interpreter.variable import VariableType, Variable, Function

class Scope():
    def __init__(self):
        self.variables = []
    def declare_variable(self, name, vtype):
        self.variables.append(Variable(name, vtype, None))
    def find_variable(self, varname):
        # TODO: hashing
        for var in self.variables:
            if var.name == varname:
                return var
        return None
