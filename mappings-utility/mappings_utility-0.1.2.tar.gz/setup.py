# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mappings_utility']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.87.0,<0.88.0',
 'pandas>=1.5.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'uvicorn>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'mappings-utility',
    'version': '0.1.2',
    'description': 'mapping utility tool for sdmx based partial mappings',
    'long_description': 'An SDMX mapping utility to generate partial key maps for referential metadata.\nAlthough not designed to do that, data mappings are also possible.\n\nThree methods are available:\n- *map_withFile* GET method (receiving the mapping source and mapping rules both as file references)\n- *map_withURN* GET method (receiving the mapping source  as file and the mapping rules as SDMX registry endpoint + mapping ID)\n- *map_json_withURN* POST method (receiving the mapping source as the body of the request in json - pandas dataframe dictionary style - and mapping rules as SDMX registry endpoint + mapping ID) (added in version 0.1.1)\n',
    'author': 'Gyorgy Gyomai',
    'author_email': 'gyorgy.gyomai@oecd.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
