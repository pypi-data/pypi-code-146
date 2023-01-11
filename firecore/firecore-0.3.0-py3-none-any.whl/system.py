import socket
from firecore.logging import get_logger
import sys
import resource

logger = get_logger(__name__)


def find_free_port() -> int:
    """find a free port for distributed training automatically
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        _host, port = s.getsockname()

    logger.debug("found a free port", port=port)
    return port


def ulimit_n_max():
    """Raise ulimit to its max value
    在某些情况下，dataloader会把文件描述符用完，使用这个函数保证实验运行
    """
    if not 'linux' in sys.platform:
        logger.warning('this is only supported on linux')
        return

    _soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_NOFILE)

    logger.debug('setting ulimit -n %d', hard_limit)
    resource.setrlimit(resource.RLIMIT_NOFILE, (hard_limit, hard_limit))
