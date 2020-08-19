class Function():
    def __init__(self, name, return_type, node):
        self.name = name
        self.return_type = return_type
        self.node = node
    def __repr__(self):
        if self.node != None:
            return "Function[{}, statements:{}]".format(self.name, len(self.node.children))
        else:
            return "Function[{}]".format(self.name)
    __str__ = __repr__
    
class BuiltinFunction(Function):
    def __init__(self, name, return_type, callback):
        Function.__init__(self, name, return_type, None)
        self.callback = callback
        
    def call(self, node):
        return self.callback(node)