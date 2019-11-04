import logging
import logging.handlers as handlers
import time
import os
import sys
from datetime import date

logFilePath = (os.path.join(os.getcwd(), "/logs/"))
logfile = logFilePath + "IU-DualCredit_Error_Log_" + str(date.today()) + ".txt"

def write_log(text):
    try:
        f = open(logfile, 'a')           
        f.write("{}\n".format(text))
    except:
        print('Can not Log File')
    return 