# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nood', 'nood.api', 'nood.monitor', 'nood.objects']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'pydantic>=1.10.4,<1.11.0',
 'pytest>=7.2.0,<7.3.0',
 'requests>=2.28.1,<2.29.0']

setup_kwargs = {
    'name': 'nood',
    'version': '0.1.4',
    'description': 'All tools you need to interact with nood.',
    'long_description': '# nood - Notifications On Demand\n\nA wrapping library for web crawlers automation.\n\n## Installation\n\nInstall `nood` with pip.\n\n```\npip install nood\n```\n\n## Example Config\n\nThe configuration for each monitor is stored in a json file. The default\ndirectory for the config file is the same as the monitor\'s script directory.\nThe default name for the config file is `config.json`, but can be configured\nindividually.\n\n```json\n{\n  "siteId": 1234,\n  "apiKey": "abcdefg1234567890",\n  "proxies": [\n    "ip:port:user:pass"\n  ],\n  "urls": [\n    "https://example.com/1",\n    "https://example.com/2"\n  ],\n  "pids": [\n    "example-pid-1",\n    "example-pid-2"\n  ]\n}\n```\n\n## Example Script\n\nFor each monitor, the `Scraper` and `Parser` class must be defined. The\nmonitoring logic is managed in the `Monitor` class which is defined by `nood`.\n\n```python\nimport requests\n\nfrom nood import monitor, objects\n\n\nclass KickzScraper(monitor.Scraper):\n    def __init__(self, url: str, **kwargs):\n        super(KickzScraper, self).__init__(url=url, **kwargs)\n\n    def download(self) -> requests.Response:\n        headers = {\n            \'user-agent\': \'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \'\n                          \'AppleWebKit/537.36 (KHTML, like Gecko) \'\n                          \'Chrome/108.0.0.0 Safari/537.36\',\n            \'referer\': \'https://www.kickz.com/.html\',\n        }\n        response = self._s.get(\n            url=self.url,\n            proxies=self.get_static_proxy(),\n            headers=headers\n        )\n\n        return response\n\n\nclass KickzParser(monitor.Parser):\n    def __init__(self):\n        super().__init__()\n\n    def parse(self, *, response: requests.Response):\n        return objects.Product(\n            url=response.url,\n            name="Name of the Product"\n        )\n\n\n\nif __name__ == "__main__":\n    monitor.Monitor.launch_tasks(scraper=KickzScraper, parser=KickzParser)\n```\n',
    'author': 'timreibe',
    'author_email': 'github@timreibe.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
