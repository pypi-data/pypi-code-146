import inspect
import datetime

class bcolors:
    HEADER = '\033[96m'
    INFO = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def console(message, status=bcolors.GREEN):
    caller = inspect.stack()[1].function
    end_status = bcolors.ENDC
    try:
        sentences = str(message).splitlines()
        for sentence in sentences:
            print("[{}] (".format(str(datetime.datetime.now()), ) + bcolors.HEADER + "{}".format(
                caller) + bcolors.ENDC + ")" + status
                  + "  {}".format(sentence)
                  + end_status)
        return True
    except Exception as e:
        print("[{}] ".format(str(datetime.datetime.now())) +
              bcolors.FAIL + "Exception caught while attempting console message: {}".format(str(e)) + end_status)
        return False

