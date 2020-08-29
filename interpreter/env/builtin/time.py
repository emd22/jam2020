from interpreter.basic_value import BasicValue
from datetime import datetime

import time

def builtin_time_sleep(arguments):
    length = arguments.arguments[0].extract_value()
    time.sleep(int(length))
    return BasicValue(length)
    
def builtin_time_now(arguments):
    time_epoch = time.mktime(datetime.today().timetuple())
    return BasicValue(time_epoch)
