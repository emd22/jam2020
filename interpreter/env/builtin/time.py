from interpreter.basic_value import BasicValue
from datetime import datetime

import time

def builtin_time_sleep(arguments):
    length = arguments.arguments[0]
    time.sleep(int(length))
    
def builtin_time_now(arguments):
    time_epoch = time.mktime(datetime.today().timetuple())
    return BasicValue(time_epoch)
