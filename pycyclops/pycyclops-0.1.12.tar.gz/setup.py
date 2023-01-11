# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cyclops',
 'cyclops.evaluate',
 'cyclops.evaluate.metrics',
 'cyclops.evaluate.metrics.functional',
 'cyclops.models',
 'cyclops.models.neural_nets',
 'cyclops.models.wrappers',
 'cyclops.monitor',
 'cyclops.monitor.datasets',
 'cyclops.monitor.gemini',
 'cyclops.monitor.gemini.mortality',
 'cyclops.process',
 'cyclops.process.feature',
 'cyclops.query',
 'cyclops.query.post_process',
 'cyclops.utils',
 'cyclops.workflow']

package_data = \
{'': ['*'],
 'cyclops.models': ['configs/*'],
 'cyclops.monitor': ['configs/gemini/*', 'configs/nihcxr/*'],
 'cyclops.monitor.datasets': ['configs/*'],
 'cyclops.query': ['configs/*']}

install_requires = \
['SQLAlchemy>=1.4.32,<2.0.0',
 'alibi-detect[torch]>=0.10.4,<0.11.0',
 'alibi[shap]>=0.8.0,<0.9.0',
 'colorama>=0.4.4,<0.5.0',
 'dask[dataframe]>=2022.9.1,<2023.0.0',
 'hydra-core>=1.2.0,<2.0.0',
 'llvmlite==0.38.0',
 'matplotlib>=3.5.1,<4.0.0',
 'pandas>=1.4.1,<2.0.0',
 'plotly==5.7.0',
 'prefect==2.0b6',
 'protobuf==3.20.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'pyarrow>=7.0.0,<8.0.0',
 'pyparsing==3.0.8',
 'python-dotenv>=0.19.2,<0.20.0',
 'seaborn>=0.11.2,<0.12.0',
 'shap>=0.40.0,<0.41.0',
 'tables>=3.7.0,<4.0.0',
 'torch>=1.11.0,<2.0.0',
 'torchxrayvision>=0.0.37,<0.0.38',
 'xgboost>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'pycyclops',
    'version': '0.1.12',
    'description': 'Framework for healthcare ML implementation',
    'long_description': "![cyclops Logo](https://github.com/VectorInstitute/cyclops/blob/main/docs/source/theme/static/cyclops_logo-dark.png?raw=true)\n\n--------------------------------------------------------------------------------\n\n[![PyPI](https://img.shields.io/pypi/v/pycyclops)](https://pypi.org/project/pycyclops)\n[![code checks](https://github.com/VectorInstitute/cyclops/actions/workflows/code_checks.yml/badge.svg)](https://github.com/VectorInstitute/cyclops/actions/workflows/code_checks.yml)\n[![integration tests](https://github.com/VectorInstitute/cyclops/actions/workflows/integration_tests.yml/badge.svg)](https://github.com/VectorInstitute/cyclops/actions/workflows/integration_tests.yml)\n[![docs](https://github.com/VectorInstitute/cyclops/actions/workflows/docs_deploy.yml/badge.svg)](https://github.com/VectorInstitute/cyclops/actions/workflows/docs_deploy.yml)\n[![codecov](https://codecov.io/gh/VectorInstitute/cyclops/branch/main/graph/badge.svg)](https://codecov.io/gh/VectorInstitute/cyclops)\n[![license](https://img.shields.io/github/license/VectorInstitute/cyclops.svg)](https://github.com/VectorInstitute/cyclops/blob/main/LICENSE)\n\n``cyclops`` is a framework for facilitating research and deployment of ML models\nin the health (or clinical) setting. It provides a few high-level APIs namely:\n\n\n* `query` - Querying EHR databases (such as MIMIC-IV)\n* `process` - Process static and temporal EHR data\n* `evaluate` - Evaluate models on clinical prediction tasks\n* `monitor` - Detect data drift relevant for clinical use cases\n\n``cyclops`` also provides a library of use-cases on clinical datasets. The implemented\nuse cases include:\n\n* Mortality decompensation prediction\n\n\n## 🐣 Getting Started\n\n### Installing cyclops using pip\n\n```bash\npython3 -m pip install pycyclops\n```\n\n## 🧑🏿\u200d💻 Developing\n\nThe development environment has been tested on ``python = 3.9``.\n\nThe python virtual environment can be set up using\n[poetry](https://python-poetry.org/docs/#installation). Hence, make sure it is\ninstalled and then run:\n\n```bash\npoetry install\nsource $(poetry env info --path)/bin/activate\n```\n\n### Contributing\nContributing to cyclops is welcomed. See [Contributing](CONTRIBUTING.md) for\nguidelines.\n\n\n## 📚 [Documentation](https://vectorinstitute.github.io/cyclops/)\n\n## 📓 Notebooks\n\nTo use jupyter notebooks, the python virtual environment can be installed and\nused inside an IPython kernel. After activating the virtual environment, run:\n\n```bash\npython3 -m ipykernel install --user --name <name_of_kernel>\n```\n\nNow, you can navigate to the notebook's ``Kernel`` tab and set it as\n``<name_of_kernel>``.\n\nTutorial notebooks in ``docs/source/tutorials`` can be useful to view the\nfunctionality of the framework.\n\n## 🎓 Citation\nReference to cite when you use CyclOps in a project or a research paper:\n```\n@article {Krishnan2022.12.02.22283021,\n\tauthor = {Krishnan, Amrit and Subasri, Vallijah and McKeen, Kaden and Kore, Ali and Ogidi, Franklin and Alinoori, Mahshid and Lalani, Nadim and Dhalla, Azra and Verma, Amol and Razak, Fahad and Pandya, Deval and Dolatabadi, Elham},\n\ttitle = {CyclOps: Cyclical development towards operationalizing ML models for health},\n\telocation-id = {2022.12.02.22283021},\n\tyear = {2022},\n\tdoi = {10.1101/2022.12.02.22283021},\n\tpublisher = {Cold Spring Harbor Laboratory Press},\n\tURL = {https://www.medrxiv.org/content/early/2022/12/08/2022.12.02.22283021},\n\tjournal = {medRxiv}\n}\n```\n",
    'author': 'Vector AI Engineering',
    'author_email': 'cyclops@vectorinstitute.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/VectorInstitute/cyclops',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
