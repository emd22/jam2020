from interpreter.basic_value import BasicValue

class SymbolInfo:
    def __init__(self, varname, decltype, value=None):
        self.varname = varname
        self.decltype = decltype
        self.value_wrapper = BasicValue(value)

class Scope():
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def declare_variable(self, name, decltype):
        self.variables[name] = SymbolInfo(name, decltype)

        return self.variables[name].value_wrapper

    def set_variable(self, name, value):
        var = self.find_variable_info(name)

        if var != None:
            var.value_wrapper.assign_value(value)

    def find_variable_info(self, name, limit=False):
        if name in self.variables:
            return self.variables[name]

        if limit or self.parent is None:
            return None

        return self.parent.find_variable_info(name)

    def find_variable_value(self, name, limit=False):
        return self.find_variable_info(name, limit).value_wrapper

    def find_variable_decltype(self, name, limit=False):
        return self.find_variable_info(name, limit).decltype
        
    def __str__(self):
        return "Scope definitions: {}".format(self.variables)
        
    __repr__ = __str__
    
class FunctionScope(Scope):
    def __init__(self):
        Scope.__init__(None)

    
