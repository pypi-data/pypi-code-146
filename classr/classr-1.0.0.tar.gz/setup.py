# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'classr',
    'version': '1.0.0',
    'description': 'Use microclassifiers in the cloud for spam detection, sentiment analysis and more.',
    'long_description': '# Classr SDK for Python\nUse microclassifiers in the cloud for spam detection, sentiment analysis and more.\n\n## Requirements\n\n- Python 3.6 or newer\n\n## Installation\n\nThe Classr SDK for Python can be installed using `pip`:\n\n```sh\npip install classr\n```\n\n## Usage\n\nTODO\n\n## Related Projects\n\nTODO\n\n## License\n\n[MIT](LICENSE) © [lambdacasserole](https://github.com/lambdacasserole).\n',
    'author': 'Saul Johnson',
    'author_email': 'saul.a.johnson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lambdacasserole/classr-py.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
