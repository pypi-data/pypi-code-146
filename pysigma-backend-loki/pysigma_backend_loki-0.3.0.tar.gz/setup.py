# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigma', 'sigma.backends.loki', 'sigma.pipelines.loki']

package_data = \
{'': ['*']}

install_requires = \
['pysigma-pipeline-sysmon>=1.0.1,<2.0.0', 'pysigma>=0.8.9,<0.9.0']

setup_kwargs = {
    'name': 'pysigma-backend-loki',
    'version': '0.3.0',
    'description': 'pySigma Loki backend',
    'long_description': "![PyPI](https://img.shields.io/pypi/v/pysigma-backend-loki)\n![Tests](https://github.com/grafana/pySigma-backend-loki/actions/workflows/test.yml/badge.svg)\n[![Coverage Status](https://coveralls.io/repos/github/grafana/pySigma-backend-loki/badge.svg?branch=main&t=lvM1Ns)](https://coveralls.io/github/grafana/pySigma-backend-loki?branch=main)\n\n# pySigma Loki Backend\n\nThis is the Loki backend for pySigma. It provides the package `sigma.backends.loki` with the `LogQLBackend` class.\n\nIt supports the following output formats:\n\n* `default`: plain Loki LogQL queries\n* `ruler`: creates Loki LogQL queries in the ruler (YAML) format for generating alerts\n\nIt includes new Loki-specific pipeline transformations:\n\n* `SetLokiStreamSelectionTransform`: adds a `logsource_loki_selection` custom attribute to a rule, which should contain a [stream selector](https://grafana.com/docs/loki/latest/logql/log_queries/#log-stream-selector) that will be used in the generated query\n* `SetLokiParserTransformation`: adds a `loki_parser` custom attribute to a rule, which should contain a [parser expression](https://grafana.com/docs/loki/latest/logql/log_queries/#parser-expression) that will be used in the generated query\n\nFurther, it contains the processing pipelines in `sigma.pipelines.loki`:\n\n* `loki_log_parser`: converts field names to logfmt labels used by Grafana\n* `loki_promtail_sysmon_message`: parse and adjust field names for Windows sysmon data produced by promtail\n  * Note: most rules lack the `sysmon` service tag, and hence this pipeline should be used in combination with the [generic sysmon pipeline](https://github.com/SigmaHQ/pySigma-pipeline-sysmon)\n\nThis backend is currently maintained by:\n\n* [Nick Moore](https://github.com/kelnage)\n* [Mostafa Moradian](https://github.com/mostafa)\n\n## Installation\n\nTo get started developing/testing pySigma-backend-loki, these steps may help you get started:\n\n1. [Install poetry](https://python-poetry.org/docs/#installation)\n2. Clone this repository and open a terminal/shell in the top-level directory\n3. Run `poetry install` to install the Python dependencies\n4. Run `poetry shell` to activate the poetry environment\n5. Check it all works by running `poetry run pytest`\n6. (Optional) If you wish to validate the generated rules using sigma\\_backend\\_tester.py, install\n   [LogCLI](https://grafana.com/docs/loki/latest/tools/logcli/)\n\n## Work in progress\n\nThese features are currently either WIP or are planned to be implemented in the near future.\n\n* Various processing pipelines for other applications and log sources\n* Generating more accurate log stream selectors based on logsource\n* Translate field names in Sigma signatures into relevant labels for Loki using pipelines\n\n## Won't implement (probably)\n\nThese features are not easily supported by the backend, and hence are unlikely to be implemented.\n\n* More complex keyword/line filter searches than ANDs of ORs\n",
    'author': 'Nick Moore',
    'author_email': 'nicholas.moore@grafana.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/grafana/pySigma-backend-loki',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
