# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fanucpy']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0',
 'opencv-contrib-python>=4.5.5,<5.0.0',
 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'fanucpy',
    'version': '0.1.8',
    'description': 'Python package for FANUC industrial robots',
    'long_description': '# fanucpy: Python package for FANUC industrial robots\n\n## Acknowledgements\nThis work was developed at the [Institute for Advanced Manufacturing at the University of Nottingham](https://www.nottingham.ac.uk/ifam/index.aspx) as a part of the [Digital Manufacturing and Design Training Network](https://dimanditn.eu/).\n\nThis project has received funding from the European Union’s Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement No 814078.\n\n## Software contents\nThe package consists of two parts: \n1. Robot interface code written in Python programming language\n2. FANUC robot controller driver (tested with R-30iB Mate Plus Controller) written in KAREL and FANUC teach pendant languages\n\nThe communication protocol between the Python package and the FANUC robot controller is depicted below:\n![Communication Protocol](https://github.com/torayeff/fanucpy/raw/main/media/CommProtocol.png)\n\n## Python package installation\n```bash\npip install fanucpy\n```\n\n## Driver installation\nFollow these [steps](https://github.com/torayeff/fanucpy/blob/main/fanuc.md) to install FANUC driver.\n\n## Usage\n### Connect to a robot:\n```python\nfrom fanucpy import Robot\n\nrobot = Robot(\n    robot_model="Fanuc",\n    host="192.168.1.100",\n    port=18735,\n    ee_DO_type="RDO",\n    ee_DO_num=7,\n)\n\nrobot.connect()\n```\n\n### Moving\n```python\n# move in joint space\nrobot.move(\n    "joint",\n    vals=[19.0, 66.0, -33.0, 18.0, -30.0, -33.0],\n    velocity=100,\n    acceleration=100,\n    cnt_val=0,\n    linear=False\n)\n\n# move in cartesian space\nrobot.move(\n    "pose",\n    vals=[0.0, -28.0, -35.0, 0.0, -55.0, 0.0],\n    velocity=50,\n    acceleration=50,\n    cnt_val=0,\n    linear=False\n)\n```\n\n### Opening/closing gripper\n```Python\n# open gripper\nrobot.gripper(True)\n\n# close gripper\nrobot.gripper(False)\n```\n\n### Querying robot state\n```python\n# get robot state\nprint(f"Current pose: {robot.get_curpos()}")\nprint(f"Current joints: {robot.get_curjpos()}")\nprint(f"Instantaneous power: {robot.get_ins_power()}")\nprint(f"Get gripper state: {robot.get_rdo(7)}")\n```\n\n\n## RobotApp\nWe introduce an experimental feature: Robot Apps. This class facilitates modularity and plug-and-produce functionality. Check the following example apps:\n\n1. [Pick and Place App](examples/PickAndPlaceApp.py)\n1. [Aruco Tracking App](examples/ArucoTrackingApp.py)\n\n## Citation\nPlease use the following to cite if you are using this library in academic publications [Towards Modular and Plug-and-Produce Manufacturing Apps](https://www.sciencedirect.com/science/article/pii/S2212827122004255)\n```\n@article{torayev2022towards,\n  title={Towards Modular and Plug-and-Produce Manufacturing Apps},\n  author={Torayev, Agajan and Mart{\\\'\\i}nez-Arellano, Giovanna and Chaplin, Jack C and Sanderson, David and Ratchev, Svetan},\n  journal={Procedia CIRP},\n  volume={107},\n  pages={1257--1262},\n  year={2022},\n  publisher={Elsevier}\n}\n```\n',
    'author': 'Agajan Torayev',
    'author_email': 'torayeff@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/torayeff/fanucpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
