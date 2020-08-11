from interpreter.variable import VariableType, Variable

class Scope():
    def __init__(self):
        self.variables = []
    def declare_variable(self, name, vtype, value):
        self.variables.append(Variable(name, vtype, value))
    def find_variable(self, varname):
        # TODO: hashing
        for var in self.variables:
            if var.name == varname:
                return var
        return None
