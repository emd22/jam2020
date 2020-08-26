from interpreter.basic_value import BasicValue

def builtin_int_add(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(int(lhs + rhs))

def builtin_int_sub(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(int(lhs - rhs))
    
def builtin_int_mul(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(int(lhs * rhs))

def builtin_int_div(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(int(lhs // rhs))

def builtin_int_bitor(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(int(lhs | rhs))

def builtin_int_bitand(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(int(lhs & rhs))

def builtin_int_bitxor(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(int(lhs ^ rhs))

def builtin_int_mod(arguments):
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(int(lhs % rhs))

from interpreter.basic_value import BasicValue

def builtin_float_add(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(float(lhs + rhs))

def builtin_float_sub(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(float(lhs - rhs))
    
def builtin_float_mul(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(float(lhs * rhs))

def builtin_float_div(arguments):
    interpreter = arguments.interpreter
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(float(lhs / rhs))
    
def builtin_float_mod(arguments):
    lhs = arguments.arguments[0].extract_value()
    rhs = arguments.arguments[1].extract_value()
    
    return BasicValue(float(lhs % rhs))
