import os

from pytest_ver import pth
from pytest_ver.lib import services


# -------------------
def pytest_addoption(parser):
    parser.addoption('--iuvmode', action='store_true', dest='iuvmode', default=False)
    parser.addoption('--cfg_path', action='store', dest='cfg_path', default=None)


# -------------------
def pytest_configure(config):
    os.environ['iuvmode'] = str(config.getoption('iuvmode'))
    if config.getoption('cfg_path') is not None:
        os.environ['PYTEST_VER_CFG'] = str(config.getoption('cfg_path'))

    pth.init()
    # uncomment to debug
    print(f'---@@@@: iuvmode={os.environ["iuvmode"]}')
    print(f'---@@@@: cfg_path={services.cfg.cfg_path} cli={config.getoption("cfg_path")}')
