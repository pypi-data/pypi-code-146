import asyncio
import calendar
import datetime
import json
import os
import sys
from dataclasses import dataclass

import importlib
import subprocess
import re
from importlib.metadata import version

import pytz
from packaging import version as version_parser
import pkg_resources
from subprocess import run
from IPython import get_ipython
import subprocess

currentfile = sys.argv[0]


def get_current_kernel(worker_id):
    if (is_in_ipynb == False):
        return worker_id

    from IPython.lib import kernel
    connection_file_path = kernel.get_connection_file()
    connection_file = os.path.basename(connection_file_path)
    kernel_id = connection_file.split('-', 1)[1].split('.')[0]
    return kernel_id


@dataclass
class Serializable:

    # The serialization function for JSON, if for some reason you really need pickle you can use it instead
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def serialize(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        return obj.__dict__

def serializeDTO(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime.date):
        return datetime.datetime.strftime(obj, "%Y-%m-%dT%H:%M:%S.%fZ")
    serialize_op = getattr(obj, "serialize", None)
    if callable(serialize_op):
        return obj.serialize(obj)
    if hasattr(obj, "__dict__"):
        return obj.__dict__

    return None

def in_ipynb():
    try:
        cfg = get_ipython().config

        if ("jupyter" in cfg['IPKernelApp']['connection_file']):
            return True
        elif ("Jupyter" in cfg['IPKernelApp']['connection_file']):
            return True
        else:
            return False
    except Exception:
        return False


is_in_ipynb = in_ipynb()

if not 'workbookDir' in globals():
    workbookDir = os.getcwd()


def get_current_plugin_code_type():
    if is_in_ipynb:
        return "ipynb"
    return "py"

def checkIfCodeContainsVersionorExit( code):
    found = False
    try:
        found = re.search('(#version:)[ ]*([0-9a-z]*\.[0-9a-z]*\.[0-9a-z]*)([\n,\\\n])', code).group(2)
    except AttributeError:
        found = False

    if not found:
        print("ERROR: You should add '#version: 1.X.X' to your file")
        sys.exit(0)
    return found

def periodInSeconds(period):
    if period.endswith("m"):
        return float(period.replace("m", "")) * 60
    if period.endswith("h"):
        return float(period.replace("h", "")) * 60 * 60
    if period.endswith("d"):
        return float(period.replace("d", "")) * 60 * 60 * 24
    if period.endswith("M"):
        return float(period.replace("M", "")) * 60 * 60 * 24 * 30
    if period.endswith("Y"):
        return float(period.replace("Y", "")) * 60 * 60 * 24 * 365
    return 60


def isFinalTimestamp(coinlibtimeframe, date, lastFinalDate = None):
    mydate = None
    lastFinal = None
    if lastFinalDate is not None:
        if isinstance(lastFinalDate, str):
            lastFinal = datetime.datetime.strptime(lastFinalDate, "%Y-%m-%dT%H:%M:%S.%fZ")
        if isinstance(lastFinalDate, int):
            lastFinal = datetime.datetime.fromtimestamp(lastFinalDate / 1000)
        if isinstance(lastFinalDate, datetime.datetime):
            lastFinal = lastFinalDate
    if isinstance(date, str):
        mydate = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    if isinstance(date, int):
        mydate = datetime.datetime.fromtimestamp(date / 1000)
    if isinstance(date, datetime.datetime):
        mydate = date

    nowdate = datetime.datetime.now()

    if mydate is not None:
        if nowdate.weekday() == mydate.weekday() and \
                nowdate.month == mydate.month and \
                nowdate.year == mydate.year:
            timestamp = calendar.timegm(mydate.utctimetuple())
            periodSeconds = periodInSeconds(coinlibtimeframe)
            restofseconds = timestamp % periodSeconds
            if restofseconds == 0 and mydate.microsecond < 999000:
                if lastFinalDate is not None:
                    timestamp = calendar.timegm(mydate.replace(second=0, microsecond=0).utctimetuple())
                    lastFinaltimestamp = int(calendar.timegm(lastFinal.replace(second=0, microsecond=0).utctimetuple()))
                    if lastFinaltimestamp == timestamp:
                        return False
                print(mydate)
                return True

    return False


class Timer:
    def __init__(self, timeframe, coinlibClass, params, callback):
        self._periodSeconds = periodInSeconds(timeframe)
        self._params = params
        self._c = coinlibClass
        self._timeframe = timeframe
        self._callback = callback
        self._maximumInterval = self._periodSeconds / 60
        if self._maximumInterval > 60:
            self._maximumInterval = 60
        self._minimumInterval = 0.02
        self._dynamicInterval = 1
        self._is_first_call = True
        self._ok = True
        self._lastFired = 0
        self._task = asyncio.ensure_future(self._job())

    def checkTimeFrame(self, mydate):
        timestamp = calendar.timegm(mydate.utctimetuple())
        timestampSeconds = timestamp
        periodSeconds = periodInSeconds(self._timeframe)
        restofseconds = timestamp % periodSeconds
        if restofseconds == 0 \
                and self._lastFired < timestampSeconds:
            self._lastFired = int(timestamp)
            return True

        return self._periodSeconds - restofseconds

    async def _job(self):
        try:
            while self._ok:
                if self._dynamicInterval < self._minimumInterval:
                    self._dynamicInterval = self._minimumInterval
                if not self._is_first_call:
                    await asyncio.sleep(self._dynamicInterval)
                mydate = datetime.datetime.now()
                timeFrameSlot = self.checkTimeFrame(mydate)
                if isinstance(timeFrameSlot, bool) and timeFrameSlot == True:
                    await self._callback(self._c, self._timeframe, datetime.datetime.now(tz=pytz.utc), self._params)
                else:
                    if timeFrameSlot < 60:
                        self._dynamicInterval = 1
                    if timeFrameSlot < 10:
                        self._dynamicInterval = 0.5
                    if timeFrameSlot < 5:
                        self._dynamicInterval = 0.05
                    if timeFrameSlot >= 60:
                        self._dynamicInterval = self._maximumInterval
                self._is_first_call = False
        except Exception as ex:
            print(ex)

    def cancel(self):
        self._ok = False
        self._task.cancel()

def createTimerWithTimestamp(callback, timeframe, c, params):
    timer = Timer(timeframe=timeframe, coinlibClass=c, params=params, callback=callback)
    return timer


def find_current_runner_file(searchFor=[".waitForJobs", ".connectAsLogic",".connectAsBroker",
                                        ".connectAsFeature", ".connectAsNotification",
                                        ".connectAsStatistic", ".connectAsStatisticMethod",
                                        ".connectCoinlib", ".connectAsBrokerSymbol"]):
    try:
        rel_path = ""
        last_path = ""
        for i in range(30):
            cur_path = sys._getframe(i).f_globals['__file__']
            code = get_current_plugin_code(cur_path)
            containsSearchFor = False
            try:
                for sf in searchFor:
                    if sf in code and sf + "\"" not in code:
                        containsSearchFor = True
            except AttributeError:
                containsSearchFor = False
                pass
            if containsSearchFor:
                rel_path = cur_path
                break
            last_path = cur_path

        cwd = os.getcwd()
        abs_path = os.path.join(cwd, rel_path)
        only_filename = os.path.splitext(os.path.basename(abs_path))[0]
        return abs_path, only_filename
    except Exception as e:
        printError("Can not find the code for your file - look if you connected coinlib Correct. (Use one of: "+",".join(searchFor)+" )")
        sys.exit(0)


def get_current_plugin_code(abs_path):
    if not is_in_ipynb:
        f = open(abs_path)
        return f.read()

    return ""

def printError(msg):
    print('\033[31m'+msg+'\033[31m')

def run_shell(shell):
    try:
        subprocess.call(['sh', shell])
    except Exception as e:
        print(e)
        pass

def pip_install(module_name: str, module_version: str):
    if in_ipynb():
        get_ipython().run_line_magic('pip', 'install $module_name==' + module_version)
    else:
        # subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        if "http:" in module_name or "https:" in module_name or "git:" in module_name:
            os.system(sys.executable+" -m pip install " + module_name )
        else:
            os.system(sys.executable+" -m pip install " + module_name + "==" + module_version)

def pip_install_or_ignore(import_name: str, module_name: str, module_version: str, shell: str = None):
    """
    This method installs some pip libraries into your module. You should enter the "import_name"
    and the "module" which should be "pip installed".

    Parameters
    --------
    import_name: str
        The name of module when you "import" it (we test this in a try catch if it exists)
    module_name: str
        The installation script. For example it could be same as "import_name" or you can install it via "git+https://yourrepo.git#subdirectory=python"
    module_version: string
        The version which should be installed - we update this version if its not the current we "upgrade" it to this version.
    """
    try:
        if "http:" in module_name or "https:" in module_name or "git:" in module_name:
            current_version = version(import_name)
        else:
            current_version = version(module_name)
        #ret_mod = importlib.import_module(import_name)
        #print([p.project_name for p in pkg_resources.working_set])

        #current_version = version(module_name)
        if version_parser.parse(current_version) != version_parser.parse(module_version):
            print("=> pip install check: updating "+import_name+" to "+module_version+" (current: "+current_version+")")
            if shell is not None:
                run_shell(shell)
            # install a newer version
            pip_install(module_name, module_version)

        return importlib.import_module(import_name)
    except ImportError:
        print("=> pip install check: missing importing of " + import_name)
        if shell is not None:
            run_shell(shell)
        pip_install(module_name, module_version)
        return False
    except Exception as e:
        print("=> pip install check: unknown error " + str(e))
        return False

def system_install_or_ignore(installation_check_shell: str, installation_code_shell: str):
    """
    This method checks if a first line of bash script can executed (for example if a library is already available on linux).
    If the first command returns -1 then the second paramter "installation_code_bash" is executed.
    So you can install linux libraries into the system if they dont exist.

    Parameters
    --------
    installation_check_shell: str
        The bash script in multiline string to check if should call second parameter
        Example:
            ls | grep YourFile  << This method returns "0" when its true and "YourFile" exists otherwise it returns 1

            When the return code is "1" (so false) then we proceed with installation. Next time it should be "0"
    installation_code_shell: str
        Code to install some library

    """
    try:

        process = subprocess.Popen(installation_check_shell, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        exit_code = process.wait()
        if exit_code != 0:
            if len(stderr) > 0:
                raise(Exception(stderr))

            process = subprocess.Popen(installation_code_shell, shell=True, stderr=subprocess.PIPE,
                                       stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            exit_code = process.wait()
            if exit_code == 0:
                return True

            if len(stderr) > 0:
                raise(Exception(stderr))

            return False

    except Exception as e:
        print("ERROR IN SHELL SCRIPT (check script): "+str(e))
        print(stderr)
        return False

    return True

def to_trendline(data: str):
    s = data.split(",")
    return {
        "x2": datetime.datetime.strptime(s[2], "%Y-%m-%dT%H:%M:%S.%fZ"),
        "y2": s[3],
        "x1": datetime.datetime.strptime(s[0], "%Y-%m-%dT%H:%M:%S.%fZ"),
        "y1": s[1],
        "type": s[4]
    }


def trendline(x2: datetime, y2, x1: datetime, y1, name: str = ""):
    x2_d = datetime.datetime.strftime(x2, "%Y-%m-%dT%H:%M:%S.%fZ")
    x1_d = datetime.datetime.strftime(x1, "%Y-%m-%dT%H:%M:%S.%fZ")
    return "" + str(x1_d) + "," + str(float(y1)) + "," + str(x2_d) + "," + str(float(y2)) + "," + name
