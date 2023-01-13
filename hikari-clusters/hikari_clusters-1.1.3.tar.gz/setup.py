# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hikari_clusters']

package_data = \
{'': ['*']}

install_requires = \
['hikari>=2.0.0.dev105,<3.0.0', 'pytest-cov>=3,<5', 'websockets>=10.1,<11.0']

setup_kwargs = {
    'name': 'hikari-clusters',
    'version': '1.1.3',
    'description': 'An advanced yet easy-to-use clustering tool for Hikari.',
    'long_description': '# hikari-clusters\n[![pypi](https://github.com/TrigonDev/hikari-clusters/actions/workflows/pypi.yml/badge.svg)](https://pypi.org/project/hikari-clusters)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/TrigonDev/hikari-clusters/main.svg)](https://results.pre-commit.ci/latest/github/TrigonDev/hikari-clusters/main)\n\n[Documentation](https://github.com/circuitsacul/hikari-clusters/wiki)\n\nhikari-clusters allows you to scale your Discord bots horizontally by using multiprocessing and websockets. This means that your bot can use multiple cores, as well as multiple VPSes.\n\nSee the #clusters channel in the hikari-py discord for help.\n\n```py\n# brain.py\nfrom hikari_clusters import Brain\n\nBrain(\n    host="localhost",\n    port=8765,\n    token="ipc token",\n    total_servers=1,\n    clusters_per_server=2,\n    shards_per_cluster=3,\n).run()\n```\n```py\n# server.py\nfrom hikari import GatewayBot\nfrom hikari_clusters import Cluster, ClusterLauncher, Server\n\nclass MyBot(GatewayBot):\n    cluster: Cluster\n\n    def __init__(self):\n        super().__init__(token="discord token")\n\n        # load modules & events here\n\nServer(\n    host="localhost",\n    port=8765,\n    token="ipc token",\n    cluster_launcher=ClusterLauncher(MyBot),\n).run()\n```\n\nRun examples with `python -m examples.<example name>` (`python -m examples.basic`)\n\n<p align="center">\n  <img src="https://us-east-1.tixte.net/uploads/files.circuitsacul.dev/hikari-clusters-diagram.jpg">\n</p>\n\n## Creating Self-Signed Certificate:\n```\nopenssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout cert.key -out cert.cert && cat cert.key cert.cert > cert.pem\n```\n',
    'author': 'Circuit',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TrigonDev/hikari-clusters',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.11',
}


setup(**setup_kwargs)
