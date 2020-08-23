from interpreter.basic_value import BasicValue

def builtin_int_add(arguments):
    interpreter = arguments[0]
    lhs = arguments[2].extract_value()
    rhs = arguments[3].extract_value()
    
    return BasicValue(lhs + rhs)

def builtin_int_sub(arguments):
    interpreter = arguments[0]
    lhs = arguments[2].extract_value()
    rhs = arguments[3].extract_value()
    
    return BasicValue(lhs - rhs)
    
def builtin_int_mul(arguments):
    interpreter = arguments[0]
    lhs = arguments[2].extract_value()
    rhs = arguments[3].extract_value()
    
    return BasicValue(lhs * rhs)

def builtin_int_div(arguments):
    interpreter = arguments[0]
    lhs = arguments[2].extract_value()
    rhs = arguments[3].extract_value()
    
    return BasicValue(lhs // rhs)
