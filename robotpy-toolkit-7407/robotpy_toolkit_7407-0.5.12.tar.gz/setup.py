# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['robotpy_toolkit_7407',
 'robotpy_toolkit_7407.motors',
 'robotpy_toolkit_7407.network',
 'robotpy_toolkit_7407.oi',
 'robotpy_toolkit_7407.pneumatics',
 'robotpy_toolkit_7407.pneumatics.pistons',
 'robotpy_toolkit_7407.sensors',
 'robotpy_toolkit_7407.sensors.color_sensors',
 'robotpy_toolkit_7407.sensors.gyro',
 'robotpy_toolkit_7407.sensors.limelight',
 'robotpy_toolkit_7407.sensors.limit_switches',
 'robotpy_toolkit_7407.sensors.photonvision',
 'robotpy_toolkit_7407.subsystem_templates',
 'robotpy_toolkit_7407.subsystem_templates.drivetrain',
 'robotpy_toolkit_7407.unum',
 'robotpy_toolkit_7407.unum.units',
 'robotpy_toolkit_7407.unum.units.custom',
 'robotpy_toolkit_7407.unum.units.others',
 'robotpy_toolkit_7407.unum.units.si',
 'robotpy_toolkit_7407.utils']

package_data = \
{'': ['*']}

install_requires = \
['robotpy-photonvision==2023.1.1b7',
 'robotpy[commands2]==2023.0.0b7',
 'wpilib==2023.1.1.0']

setup_kwargs = {
    'name': 'robotpy-toolkit-7407',
    'version': '0.5.12',
    'description': "FRC Wired Boars Team 7407's Toolkit for usage with RobotPy",
    'long_description': 'None',
    'author': 'Sidharth Rao',
    'author_email': 'sidharthmrao@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
