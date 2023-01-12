import multiprocessing
import os
import platform
import psutil
import pynvml

try:
    pynvml.nvmlInit()
except Exception:
    pass

def get_os() -> str:
    return platform.system()

def get_python_version() -> str:
    return platform.python_version()

def get_gpu() -> str:
    try:
        return pynvml.nvmlDeviceGetName(pynvml.nvmlDeviceGetHandleByIndex(0)).decode("utf-8")
    except Exception:
        return "no gpu"

def get_gpu_count() -> int:
    try:
        return pynvml.nvmlDeviceGetCount()
    except Exception:
        return 0

def get_cpu_count() -> int:
    return multiprocessing.cpu_count()

def get_hostname() -> str:
    return platform.node()

def get_system_cpu() -> float:
    return psutil.cpu_percent()

def get_system_disk() -> float:
    return psutil.disk_usage(os.path.sep).used / (2**30)

def get_system_memory() -> float:
    return psutil.virtual_memory().used / (2**30)

def get_system_proc_cpu_threads() -> int:
    pid = os.getpid() # get pid
    proc = psutil.Process(pid)
    return proc.num_threads()

def get_system_proc_memory_rss_mb() -> float:
    pid = os.getpid() # get pid
    proc = psutil.Process(pid)
    return proc.memory_info().rss / 1048576.0

def get_system_proc_memory_percent() -> float:
    pid = os.getpid() # get pid
    proc = psutil.Process(pid)
    return proc.memory_percent()

def get_system_memory_available_mb() -> float:
    return psutil.virtual_memory().available / 1048576.0


def is_notebook() -> bool:
    try:
        if 'google.colab' in str(get_ipython()):
            return True

        shell  = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


def print_progress(iteration: int, total: int, prefix: str = 'Loading', suffix: str = '', bar_length: int = 30):
    # progressBar를 출력
    if total == 0:
        percent = 100
        filled_length = bar_length
    else:
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    text = "%s |%s| [%s%%] %s" % (prefix, bar, percent, suffix)
    print('\r' + ' ' * 200, end='', flush=True) #jupyter에서 남아있는 부분을 삭제
    print('\r' + text, end='', flush=True)

    if percent == 100:
        print("\r\n")



from functools import wraps
def login_required(original_function):
    from deepdriver import logger
    ''' deepdriver 로그인 체크 '''
    @wraps(original_function)
    def wrapper(*args, **kwargs):
        from deepdriver.sdk.interface.interface import get_stub
        stub = get_stub()
        if not stub:
            logger.info("please log in first")
            raise Exception("Login required.")
        return original_function(*args, **kwargs)

    return wrapper


def init_required(original_function):
    from deepdriver import logger
    ''' deepdriver init() 체크 '''
    @wraps(original_function)
    def wrapper(*args, **kwargs):
        from deepdriver.sdk.data_types.run import get_run
        run = get_run()
        if not run:
            logger.info("please call deepdriver.init() first")
            raise Exception("Deepdriver not inited")
        return original_function(*args, **kwargs)

    return wrapper
