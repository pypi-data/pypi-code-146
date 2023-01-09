# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['psa_car_controller',
 'psa_car_controller.common',
 'psa_car_controller.psa',
 'psa_car_controller.psa.connected_car_api',
 'psa_car_controller.psa.connected_car_api.api',
 'psa_car_controller.psa.connected_car_api.models',
 'psa_car_controller.psa.otp',
 'psa_car_controller.psa.setup',
 'psa_car_controller.psacc',
 'psa_car_controller.psacc.application',
 'psa_car_controller.psacc.model',
 'psa_car_controller.psacc.repository',
 'psa_car_controller.psacc.utils',
 'psa_car_controller.web',
 'psa_car_controller.web.tools',
 'psa_car_controller.web.view']

package_data = \
{'': ['*'],
 'psa_car_controller.psacc': ['resources/*'],
 'psa_car_controller.web': ['assets/*', 'assets/images/*', 'assets/sprites/*']}

install_requires = \
['ConfigUpdater>=3.0',
 'Flask>=1.0.4',
 'Werkzeug>=1.0.0',
 'androguard>=3.3.5,<4.0.0',
 'argparse>=1.4.0,<2.0.0',
 'certifi>=14.05.14',
 'cryptography>=2.6',
 'dash-bootstrap-components>=1',
 'dash-daq>=0.5.0,<0.6.0',
 'dash>=2',
 'geojson>=2.5.0,<3.0.0',
 'oauth2-client>=1.2.1,<2.0.0',
 'paho-mqtt>=1.5.0',
 'pandas>=0.23',
 'plotly>=5',
 'pycryptodomex>=3.9.0,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'python-dateutil>=2.5.3',
 'pytz>=2021.0,<2022.0',
 'requests>=2.27.1,<3.0.0',
 'reverse-geocode>=1.4.1,<2.0.0',
 'ruamel.yaml>=0.15.0',
 'single-source>=0.3.0,<0.4.0',
 'six>=1.10',
 'urllib3>=1.15.1']

entry_points = \
{'console_scripts': ['psa-car-controller = psa_car_controller.__main__:main']}

setup_kwargs = {
    'name': 'psa-car-controller',
    'version': '3.0.8',
    'description': 'This is a python program to control a psa car with connected_car v4 api.',
    'long_description': 'None',
    'author': 'Florian Bezannier',
    'author_email': 'florian.bezannier@hotmail.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/flobz/psa_car_controller',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
