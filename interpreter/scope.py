from interpreter.variable import VariableType, Variable, Function

class Scope():
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def declare_variable(self, name, vtype, value):
        self.variables[name] = Variable(name, vtype, value)

    def find_variable(self, varname):
        if varname in self.variables:
            return self.variables[varname]

        if self.parent is None:
            return None

        return self.parent.find_variable(varname)
