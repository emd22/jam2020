class Function():
    def __init__(self, name, return_type, node):
        self.name = name
        self.return_type = return_type
        self.node = node
    def __repr__(self):
        return "Function"
    __str__ = __repr__

class BuiltinFunctionArguments(Function):
    def __init__(self, interpreter, this_object, arguments, node):
        self.interpreter = interpreter
        self.this_object = this_object
        self.arguments = arguments
        self.node = node

class BuiltinFunction(Function):
    def __init__(self, name, return_type, callback):
        Function.__init__(self, name, return_type, None)
        self.callback = callback
        
    def call(self, args):
        if not isinstance(args, BuiltinFunctionArguments):
            raise Exception("BuiltinFunction.call expects args as BuiltinFunctionArguments")
        return self.callback(args)

    def compare_value(self, other):
        return self == other

    def __repr__(self):
        return "BuiltinFunction[{}]".format(self.name)
    __str__ = __repr__
