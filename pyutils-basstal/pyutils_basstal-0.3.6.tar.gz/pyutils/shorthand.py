import sys

######################
######################
#       简写      #
######################
######################


def is_win():
    return sys.platform.lower().startswith('win')


def is_macOS():
    return sys.platform.lower().startswith('darwin')


def is_admin_win():
    """检查当前是否处在 windows 管理员模式下

    Returns:
        bool: 处在 windows 管理员模式
    """
    if is_win():
        import ctypes
        import os
        try:
            return os.getuid() == 0
        except AttributeError:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
    return False
