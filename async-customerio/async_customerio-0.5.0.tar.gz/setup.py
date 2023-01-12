# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_customerio']

package_data = \
{'': ['*']}

install_requires = \
['httpx<1.0.0']

setup_kwargs = {
    'name': 'async-customerio',
    'version': '0.5.0',
    'description': 'Async CustomerIO Client - a Python client to interact with CustomerIO in an async fashion.',
    'long_description': '# async-customerio is a lightweight asynchronous client to interact with CustomerIO\n[![PyPI download month](https://img.shields.io/pypi/dm/async-customerio.svg)](https://pypi.python.org/pypi/async-customerio/)\n[![PyPI version fury.io](https://badge.fury.io/py/async-customerio.svg)](https://pypi.python.org/pypi/async-customerio/)\n[![PyPI license](https://img.shields.io/pypi/l/async-customerio.svg)](https://pypi.python.org/pypi/async-customerio/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/async-customerio.svg)](https://pypi.python.org/pypi/async-customerio/)\n[![CI](https://github.com/healthjoy/async-customerio/actions/workflows/ci.yml/badge.svg)](https://github.com/healthjoy/async-customerio/actions/workflows/ci.yml)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/3629b50827ef4e89ba0eaa5c09584273)](https://www.codacy.com/gh/healthjoy/async-customerio/dashboard?utm_source=github.com&utm_medium=referral&utm_content=healthjoy/async-customerio&utm_campaign=Badge_Coverage)\n\n  * Free software: MIT license\n  * Requires: Python 3.7+\n\n## Features\n\n  * Fully async\n  * Interface preserved as Official Python Client `customerio` has\n  * Send push notification\n  * Send messages\n\n## Installation\n```shell script\n$ pip install async-customerio\n```\n\n## Getting started\n```python\nimport asyncio\n\nfrom async_customerio import AsyncCustomerIO, Regions\n\n\nasync def main():\n    site_id = "Some-id-gotten-from-CustomerIO"\n    api_key = "Some-key-gotten-from-CustomerIO"\n    cio = AsyncCustomerIO(site_id, api_key, region=Regions.US)\n    await cio.identify(id=5, email="customer@example.com", first_name="John", last_name="Doh", subscription_plan="premium")\n    await cio.track(customer_id=5, name="product.purchased", product_sku="XYZ-12345", price=23.45)\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\n#### Instantiating `AsyncCustomerIO` object\n\nCreate an instance of the client with your [Customer.io credentials](https://fly.customer.io/settings/api_credentials).\n\n```python\n\nfrom async_customerio import AsyncCustomerIO, Regions\n\n\ncio = AsyncCustomerIO(site_id, api_key, region=Regions.US)\n```\n\n`region` is optional and takes one of two values — `Regions.US` or `Regions.EU`. If you do not specify your region, we assume\nthat your account is based in the US (`Regions.US`). If your account is based in the EU and you do not provide the correct region\n(`Regions.EU`), we\'ll route requests to our EU data centers accordingly, however this may cause data to be logged in the US.\n\n## License\n\n``async-customerio`` is offered under the MIT license.\n\n## Source code\n\nThe latest developer version is available in a GitHub repository:\n[https://github.com/healthjoy/async-customerio](https://github.com/healthjoy/async-customerio)\n',
    'author': 'Aleksandr Omyshev',
    'author_email': 'oomyshev@healthjoy.com',
    'maintainer': 'Healthjoy Developers',
    'maintainer_email': 'developers@healthjoy.com',
    'url': 'https://github.com/healthjoy/async-customerio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.15,<3.12',
}


setup(**setup_kwargs)
