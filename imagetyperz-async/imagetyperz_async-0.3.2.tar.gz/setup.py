# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imagetyperz', 'imagetyperz.util']

package_data = \
{'': ['*']}

modules = \
['LICENSE', 'CHANGELOG']
install_requires = \
['httpx>=0.15.0']

setup_kwargs = {
    'name': 'imagetyperz-async',
    'version': '0.3.2',
    'description': 'Asynchronous client for the ImageTyperz API',
    'long_description': "# imagetyperz-async\n\nAn asynchronous client for the [ImageTyperz CAPTCHA-solving API](http://imagetyperz.com/).\n\n[httpx](https://github.com/encode/httpx) powers the HTTP requests.\n\n**At the moment, only image CAPTCHAS and reCAPTCHAs are supported.**\n\n\n# Installation\n\n```bash\npip install imagetyperz-async\n```\n\n\n# Usage\n\n```python\nimport asyncio\n\nfrom imagetyperz import ImageTyperzClient, reCAPTCHAType\nfrom imagetyperz.exceptions import NotDecoded\n\nasync def demo():\n    ###\n    # Context manager will handle the closing of connections in the underlying\n    # httpx AsyncClient at block end.\n    #\n    # Alternatively, `await ita.aclose()` may be manually called to perform\n    # cleanup.\n    #\n    # If no cleanup is performed, a warning may be emitted at Python exit.\n    #\n    async with ImageTyperzClient('6F0848592604C9E14F0EBEA7368493C5') as ita:\n        print(await ita.retrieve_balance())\n        #: 8.8325\n\n        # Submit reCAPTCHA job\n        job_id = await ita.submit_recaptcha(\n            page_url='https://example.com/login',\n            site_key='scraped-site-key',\n            recaptcha_type=reCAPTCHAType.INVISIBLE,\n        )\n        print(job_id)\n        #: 176140709\n\n        # Check for results of the reCAPTCHA job\n        while True:\n            try:\n                g_response = await ita.retrieve_recaptcha(job_id)\n            except NotDecoded:\n                await asyncio.sleep(5)\n                continue\n            else:\n                print(g_response)\n                #: 03AGdBq25hDTCjOq4QywdrY...\n                break\n\n        # Alternatively, use complete_recaptcha to automatically handle the polling\n        # for results — returning with the result when ready.\n        g_response = await ita.complete_recaptcha(\n            page_url='https://example.com/login',\n            site_key='scraped-site-key',\n            recaptcha_type=reCAPTCHAType.INVISIBLE,\n        )\n        print(g_response)\n        #: 03AGdBq25hDTCjOq4QywdrY...\n```\n",
    'author': 'Zach "theY4Kman" Kanzler',
    'author_email': 'they4kman@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/theY4Kman/imagetyperz-async',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
