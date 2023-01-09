# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydevmgr_elt',
 'pydevmgr_elt.base',
 'pydevmgr_elt.devices',
 'pydevmgr_elt.devices.adc',
 'pydevmgr_elt.devices.ccssim',
 'pydevmgr_elt.devices.drot',
 'pydevmgr_elt.devices.lamp',
 'pydevmgr_elt.devices.motor',
 'pydevmgr_elt.devices.piezo',
 'pydevmgr_elt.devices.sensor',
 'pydevmgr_elt.devices.shutter',
 'pydevmgr_elt.devices.time',
 'pydevmgr_elt.scripts',
 'pydevmgr_elt.tests_with_tins']

package_data = \
{'': ['*'], 'pydevmgr_elt': ['resources/*']}

install_requires = \
['jinja2>=3.1.2,<4.0.0', 'pydevmgr-ua==0.6.a1']

entry_points = \
{'console_scripts': ['pydevmgr_dump = pydevmgr_elt.scripts.dump:main']}

setup_kwargs = {
    'name': 'pydevmgr-elt',
    'version': '0.6a3',
    'description': 'pydevmgr pluggin for Elt devices',
    'long_description': '\nThis python package is used to handle ELT standard devices directly from python objects and through OPC-UA. \n\nThe package is intended to be used when a full instrument ELT software is not available but scripting needs to be done on devices and using the Low Level ELT software (Running on Beckhoff PLC). \nA good exemple of the use case is making sequences of initialisation and movement of motors for AIT purposes without the\nneed to buil a high level ELT software. \n\nThe documentation (for version >=0.3) is [here](https://pydevmgr-elt.readthedocs.io/en/latest/index.html)     \n\nSources are [here](https://github.com/efisoft-elt/pydevmgr_elt)\n\n\n# Install\n\n```bash\n> pip install pydevmgr_elt \n```\n\nFrom sources :\n\n```bash\n> git clone https://github.com/efisoft-elt/pydevmgr_elt\n> cd pydevmgr_elt \n> python setup.py install\n```\n\n\n# Basic Usage\n\n(since v0.5)\n\n```python \nfrom pydevmgr_elt import Motor, wait\n\n\nwith Motor(\'motor1\', address="opc.tcp://192.168.1.11:4840", prefix="MAIN.Motor1") as m1:\n    wait(m1.move_abs(7.0,1.0), lag=0.1)\n    print( "position is", m1.stat.pos_actual.get() )\n\n```\n\nCan also be done in the old way: \n\n```python\n\nfrom pydevmgr_elt import Motor, wait\nm1 = Motor(\'motor1\', address="opc.tcp://192.168.1.11:4840", prefix="MAIN.Motor1")\n\ntry:\n    m1.connect()    \n    wait(m1.move_abs(7.0,1.0), lag=0.1)\n    print( "position is", m1.stat.pos_actual.get() )\nfinally:\n    m1.disconnect()\n```\n\n```python \nfrom pydevmgr_elt import Motor, DataLink\n\nm1 = Motor(\'motor1\', address="opc.tcp://152.77.134.95:4840", prefix="MAIN.Motor1")\n\nm1_data = Motor.Data() # m1_data is a structure built with default value\nm1_dl = DataLink(m1, m1_data) # create a data link use to fill m1_data to real hw values\n\nwith m1: # with conexte manager open/close a connection  \n    m1_dl.download()\n    print( m1_data.stat.pos_actual,   m1_data.stat.pos_error  )\n```\n\nOpen from an elt yaml configuration file as defined in ELT IFW v3\n\n```python\nfrom pydevmgr_elt import open_elt_device\nmotor1 = open_elt_device( "tins/motor1.yml" )\n```\n',
    'author': 'Sylvain Guieu',
    'author_email': 'sylvain.guieu@univ-grenoble-alpes.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
