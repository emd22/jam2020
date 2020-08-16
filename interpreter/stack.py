class Stack():
    def __init__(self):
        self.stack = []
        
    def push(self, value):
        self.stack.append(value)
        
    def pop(self, expected_type=None):
        val = self.stack.pop()
        if (expected_type != None and expected_type != type(val)):
            raise Exception('Stack value({}) != expected value({})'.format(type(val), expected_type))
        return val
