# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydevmgr_core',
 'pydevmgr_core.base',
 'pydevmgr_core.misc',
 'pydevmgr_core.tests',
 'pydevmgr_core.trash',
 'pydevmgr_core_ui']

package_data = \
{'': ['*']}

install_requires = \
['py-expression-eval>=0.3.14,<0.4.0',
 'pydantic>=1.9,<2.0',
 'systemy>=0.1.1,<0.2.0',
 'valueparser>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'pydevmgr-core',
    'version': '0.6a1',
    'description': 'Python package to handle distributed device handling',
    'long_description': '\nThis python package is used as a core engine for any pydevmgr high level package. \n\nThe documentation is on its way, but one may be interested to higher level package such as \n- [pydevmgr_ua](https://github.com/efisoft-elt/pydevmgr_ua)\n- [pydevmgr_elt](https://github.com/efisoft-elt/pydevmgr_elt)\n\n\nPython package to by used as substitute of a real device manager running in a ELT-Software environment when the full ELT-Software environment cannot be used. \n\n\n\nSources are [here](https://github.com/efisoft-elt/pydevmgr_core)\n\n\n# Install\n\n```bash\n> pip install pydevmgr_core \n```\n\n# Basic Usage\n\npydevmgr_core is not indented to be used directly but used by other pydevmgr related package as a core engine. \n\nFor usage here is an example using pydevmgr_ua to access an OPC-UA node : \n\n```python\nfrom pydevmgr_ua import UaRpc, UaNode, UaCom\nfrom pydevmgr_core.nodes import InsideInterval\nimport time \n\ncom = UaCom(address="opc.tcp://192.168.1.11:4840", prefix="MAIN")\n\ntarget = 7.0\n\nmove = UaRpc( com=com, suffix="Motor1.RPC_MoveAbs", args_parser=[float, float])\npos = UaNode( com=com,  suffix="Motor1.stat.lrPosActual" )\ntest = InsideInterval( node = pos, min=target-0.1, max=target+0.1 )\n\n\ntry:\n    com.connect()\n    move.call( 7.0, 1 )\n    while not test.get():\n        time.sleep(0.1)\n\n    print( "posisiotn is", pos.get() )\nfinally:\n    com.disconnect()\n\n```\n\nOr using the highest level dedicated for ELT devices: \n\n\n```python \nfrom pydevmgr_elt import Motor, wait\nm1 = Motor(\'motor1\', address="opc.tcp://192.168.1.11:4840", prefix="MAIN.Motor1")\ntry:\n    m1.connect()    \n    wait(m1.move_abs(7.0,1.0), lag=0.1)\n    print( "position is", m1.stat.pos_actual.get() )\nfinally:\n    m1.disconnect()\n```\n',
    'author': 'Sylvain Guieu',
    'author_email': 'sylvain.guieu@univ-grenoble-alpes.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
