# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydevmgr_ua']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=39.0.0,<40.0.0',
 'opcua>=0.98.13,<0.99.0',
 'pydevmgr-core==0.6.a1']

setup_kwargs = {
    'name': 'pydevmgr-ua',
    'version': '0.6a1',
    'description': 'pydevmgr plugin to handle opc-ua communication',
    'long_description': '\npydevmgr package dedicated for generic client communication with OPC-UA. \n\nThe documentation is in progress. \n\nOne may be interested to higher level package such as \n- [pydevmgr_elt](https://github.com/efisoft-elt/pydevmgr_elt)\n\n\nPython package to by used as substitute of a real device manager running in a ELT-Software environment when the full ELT-Software environment cannot be used. \n\n\n\nSources are [here](https://github.com/efisoft-elt/pydevmgr_ua)\n\n\n# Install\n\n```bash\n> pip install pydevmgr_ua\n```\n\n# Basic Usage\n\n\n\n```python\nfrom pydevmgr_ua import UaRpc, UaNode, UaCom\nfrom pydevmgr_core.nodes import InsideInterval\nimport time \n\ncom = UaCom(address="opc.tcp://192.168.1.11:4840", prefix="MAIN")\n\ntarget = 7.0\n\nmove = UaRpc( com=com, suffix="Motor1.RPC_MoveAbs", arg_parsers=[float, float])\npos = UaNode( com=com,  suffix="Motor1.stat.lrPosActual" )\ntest = InsideInterval( node = pos, min=target-0.1, max=target+0.1 )\n\n\ntry:\n    com.connect()\n    move.call( 7.0, 1 )\n    while not test.get():\n        time.sleep(0.1)\n\n    print( "posisiotn is", pos.get() )\nfinally:\n    com.disconnect()\n\n```\n',
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
