# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nowpayments', 'nowpayments.models']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'nowpayments',
    'version': '1.3.3',
    'description': 'A Python wrapper for the NOWPayments API',
    'long_description': '# NOWPayments-Python-API\n\n[![CodeQL](https://github.com/Ventura94/NOWPayments-Python-API/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Ventura94/NOWPayments-Python-API/actions/workflows/codeql-analysis.yml)\n[![Pylint](https://github.com/Ventura94/NOWPayments-Python-API/actions/workflows/pylint.yml/badge.svg)](https://github.com/Ventura94/NOWPayments-Python-API/actions/workflows/pylint.yml)\n[![Python application](https://github.com/Ventura94/NOWPayments-Python-API/actions/workflows/python-app.yml/badge.svg)](https://github.com/Ventura94/NOWPayments-Python-API/actions/workflows/python-app.yml)\n[![Python package](https://github.com/Ventura94/NOWPayments-Python-API/actions/workflows/python-package.yml/badge.svg)](https://github.com/Ventura94/NOWPayments-Python-API/actions/workflows/python-package.yml)\n[![Upload Python Package](https://github.com/Ventura94/NOWPayments-Python-API/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Ventura94/NOWPayments-Python-API/actions/workflows/python-publish.yml)\n[![codecov](https://codecov.io/gh/Ventura94/NOWPayments-Python-API/branch/main/graph/badge.svg?token=Z7NIDJI2LD)](https://codecov.io/gh/Ventura94/NOWPayments-Python-API)\n[![Black](https://github.com/Ventura94/NOWPayments-Python-API/actions/workflows/black.yml/badge.svg)](https://github.com/Ventura94/NOWPayments-Python-API/actions/workflows/black.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nA Python wrapper for the [NOWPayments API](https://documenter.getpostman.com/view/7907941/S1a32n38?version=latest). \n\nThe api call descriptions are from the official documentation.\n\n## Getting Started\nBefore using the NOWPayments API, sign up for a [API key here](https://nowpayments.io/).\n\nIf you want to use the Sandbox, request your [API key here](https://account-sandbox.nowpayments.io/).\n\n\nTo install the wrapper, enter the following into the terminal.\n```bash\npip install nowpayments\n```\n\nEvery api call requires this api key. Make sure to use this key when getting started. \n```python\nfrom nowpayments import NOWPayments\npayment = NOWPayments("API_KEY")\n\nstatus = payment.get_api_status()\n```\nSandbox is used in the same way in correspondence with the documentation as follows.\n\n```python\nfrom nowpayments import NOWPaymentsSandbox\n\npayment = NOWPaymentsSandbox("SANDBOX_API_KEY")\n\nstatus = payment.get_api_status()\n```\n',
    'author': 'Arian Ventura Rodríguez',
    'author_email': 'arianventura94@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Ventura94/NOWPayments-Python-API',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
