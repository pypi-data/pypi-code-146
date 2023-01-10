import os
import sys


class OSInfo:

    s_os_type = 'Unknown'

    @staticmethod
    def os_type():
        return os.name

    @staticmethod
    def cpu_count():
        return os.cpu_count()

    @staticmethod
    def uname():
        return os.uname()


def count_py_files_in_folder(dirname):

    if os.path.exists(dirname):
        count = 0
        for root, dirs, files in os.walk(dirname):
            count += len([f for f in files if f.endswith('.py')])
        if count > 0:
            print('Directory "{}" has {} python files'.format(dirname, count))
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)
        if os.path.isdir(path):
            count_py_files_in_folder(path)


def demo():

    osinfo = OSInfo()

    print('################################################################')
    print('OS Type:\t{}'.format(osinfo.os_type()))
    print('CPU Count:\t{}'.format(osinfo.cpu_count()))
    print('Nodename:\t{}'.format(osinfo.uname().nodename))
    print('Sysname:\t{}'.format(osinfo.uname().sysname))
    print('Machine:\t{}'.format(osinfo.uname().machine))
    print('Release:\t{}'.format(osinfo.uname().release))
    # print('Version:\t{}'.format(osinfo.uname().version))
    print('################################################################')


if __name__ == '__main__':

    demo()

    # count_py_files_in_folder('/Users/joe/code/gogs/zyz')
    count_py_files_in_folder('.')
