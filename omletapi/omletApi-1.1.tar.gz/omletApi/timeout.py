import time 
from omletApi.errors import *

class Timeout:

    def __init__(self, timeout):

        try:
            time.sleep(timeout)
        except:
            raise TimeoutError("'timeout' not int!")

local_time = time.strftime(

    "%d/%m/%Y %H:%M:%S",
     time.localtime()
     
)
