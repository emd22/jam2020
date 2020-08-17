from interpreter.variable import VariableType, Variable, Function

class Scope():
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def declare_variable(self, name, vtype):
        self.variables[name] = Variable(name, vtype, None)
        return self.variables[name]

    def find_variable(self, varname, limit=False):
        if varname in self.variables:
            return self.variables[varname]


        if limit or self.parent is None:
            return None

        return self.parent.find_variable(varname)
        
    def __str__(self):
        return "Scope definitions: {}".format(self.variables)
        
    __repr__ = __str__
    
class FunctionScope(Scope):
    def __init__(self):
        Scope.__init__(None)

    
