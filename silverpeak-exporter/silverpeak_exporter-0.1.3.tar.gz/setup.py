# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['silverpeak_exporter']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0',
 'prometheus-client==0.15.0',
 'pyedgeconnect==0.15.3a1.dev0',
 'requests==2.28.1',
 'tomli==2.0.1']

entry_points = \
{'console_scripts': ['spexporter = silverpeak_exporter.main:main']}

setup_kwargs = {
    'name': 'silverpeak-exporter',
    'version': '0.1.3',
    'description': 'Prometheus exporter for Silverpeak SD-WAN Appliances.',
    'long_description': '![Release](https://img.shields.io/github/v/tag/ipHeaders/silverpeak-prometheus)\n![License](https://img.shields.io/github/license/ipHeaders/silverpeak-prometheus)\n![Open Issues](https://img.shields.io/github/issues/ipHeaders/silverpeak-prometheus)\n![](https://img.shields.io/github/languages/top/ipHeaders/silverpeak-prometheus)\n![](https://img.shields.io/pypi/pyversions/silverpeak-exporter)\n![Docker Pulls](https://img.shields.io/docker/pulls/ipheaders/silverpeak-prometheus)\n[![Downloads](https://static.pepy.tech/personalized-badge/silverpeak-exporter?period=total&units=none&left_color=grey&right_color=orange&left_text=PyPI%20Downloads)](https://pepy.tech/project/silverpeak-exporter)\n\n# silverpeak-prometheus-exporter\nSilverpeak/Aruba SD-WAN Prometheus Exporter, this tool is to query the Silverpeak/Aruba SD-WAN orchestrator export the metrics to a prometheus database.\n\n## Requierements\n\n- Orchestraor API Key\n- Python3.9>=\n\n## Installation Methods\n- Installing using [Pypi](https://github.com/ipHeaders/silverpeak-prometheus/tree/main/docs/installing_using_pypi.md)\n- Installing directly from [Github](https://github.com/ipHeaders/silverpeak-prometheus/tree/main/docs/installing_from_github.md)\n- Running on [Container](https://github.com/ipHeaders/silverpeak-prometheus/tree/main/docs/running_on_container.md)\n\n## References\n- Avaiable Exposed Metrics [Metrics](https://github.com/ipHeaders/silverpeak-prometheus/tree/main/docs/metrics.md)\n- DockerHub Project [Docker](https://hub.docker.com/repository/registry-1.docker.io/ipheaders/silverpeak-prometheus/general)\n- Grafana Dashboard [Grafana](https://grafana.com/grafana/dashboards/17745-silverpeak-exporter/)\n\n## Grafana Example\n### Orchestrator\n![alt text](docs/grafana_orch.png)\n\n### Appliances\n![alt text](docs/grafana_appliace.png)\n\n## Maintainer\n[IPheaders](https://github.com/ipHeaders)',
    'author': 'IP Headers',
    'author_email': 'ipHeaders@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
