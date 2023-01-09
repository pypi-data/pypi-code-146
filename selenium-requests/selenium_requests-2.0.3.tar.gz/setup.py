# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seleniumrequests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0',
 'selenium>=4.3.0,<5.0.0',
 'tldextract>=3.1.1,<4.0.0']

setup_kwargs = {
    'name': 'selenium-requests',
    'version': '2.0.3',
    'description': 'Extends Selenium WebDriver classes to include the request function from the Requests library, while doing all the needed cookie and request headers handling.',
    'long_description': 'Selenium Requests\n=================\nExtends Selenium WebDriver classes to include the\n[request](http://docs.python-requests.org/en/latest/api/#requests.request) function from the\n[Requests](http://python-requests.org/) library, while doing all the needed cookie and request headers handling.\n\nBefore the actual request is made, a local HTTP server is started that serves a single request made by the webdriver\ninstance to get the "standard" HTTP request headers sent by this webdriver; these are cached (only happens once during\nits lifetime) and later used in conjunction with the Requests library to make the requests look identical to those that\nwould have been sent by the webdriver. Cookies held by the webdriver instance are added to the request headers and those\nreturned in a response automatically set for the webdriver instance.\n\n\nFeatures\n--------\n * Determines and sends the default HTTP headers (User-Agent etc.) for the chosen WebDriver\n * Manages cookies bidirectionally between requests and Selenium\n * Switches to already existing window handles or temporarily creates them to work with the webdriver\'s cookies when\n   making a request\n * All operations preserve the original state of the WebDriver (active window handle and window handles)\n * Tested to work with Selenium (v4.1.0) using Mozilla Firefox (v97.0) and Chromium (v98.0.4758.80)\n\n\nUsage\n-----\n```python\n# Import any WebDriver class that you would usually import from\n# selenium.webdriver from the seleniumrequests module\nfrom seleniumrequests import Firefox\n\n# Simple usage with built-in WebDrivers:\nwebdriver = Firefox()\nresponse = webdriver.request(\'GET\', \'https://www.google.com/\')\nprint(response)\n\n\n# More complex usage, using a WebDriver from another Selenium-related module:\nfrom seleniumrequests.request import RequestsSessionMixin\nfrom someothermodule import CustomWebDriver\n\n\nclass MyCustomWebDriver(RequestsSessionMixin, CustomWebDriver):\n    pass\n\n\ncustom_webdriver = MyCustomWebDriver()\nresponse = custom_webdriver.request(\'GET\', \'https://www.google.com/\')\nprint(response)\n```\n\n\nInstallation\n------------\n```pip install selenium-requests```\n\n\nRemote WebDriver\n----------------\nWhen using `webdriver.Remote` it is very likely that the HTTP proxy server spawned by `selenium-requests` does not run\non the same machine. By default, the webdriver tries to access the proxy server under `127.0.0.1`. This can be changed\nby passing the `proxy_host=` argument with the correct IP or hostname to the webdriver.\n\n```python\ndriver = seleniumrequests.Remote(\n    \'http://192.168.101.1:4444/wd/hub\',\n    options=chrome_options,\n    proxy_host=\'192.168.101.2\'\n)\n```\n',
    'author': 'Chris Braun',
    'author_email': 'cryzed@googlemail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
