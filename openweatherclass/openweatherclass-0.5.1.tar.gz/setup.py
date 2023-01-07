# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openweatherclass']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0', 'requests==2.28.1']

setup_kwargs = {
    'name': 'openweatherclass',
    'version': '0.5.1',
    'description': 'An implementation of the Openweather API in Python.',
    'long_description': "# A Python implementation of the Open Weather API \n\nTo use ➡️\n\n* install from [PyPi](https://pypi.org/project/openweatherclass/).\n\n[OpenWeather Homepage](https://openweathermap.org/)\n\n```shell\npip install openweatherclass\n```\n\n* Get an [API](https://openweathermap.org/api) Key\n\n* Initiate the class\n\n```python\nimport openweatherclass as owc\n\nweather = owc.OpenWeatherClass(api_key=API_KEY, zipcode='02188', units='imperial')\nprint(weather.geo_data['name'])\nprint(weather.weather_data['current']['temp'])\n```\n",
    'author': 'Brian Hudson',
    'author_email': 'reallybrianhudson@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bearhudson/OWAlert',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
