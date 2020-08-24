from interpreter.basic_value import BasicValue

def builtin_int_add(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(lhs + rhs)

def builtin_int_sub(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(lhs - rhs)
    
def builtin_int_mul(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(lhs * rhs)

def builtin_int_div(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(lhs // rhs)
