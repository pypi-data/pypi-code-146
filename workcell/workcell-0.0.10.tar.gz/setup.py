# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['workcell',
 'workcell.api',
 'workcell.cli',
 'workcell.core',
 'workcell.integrations.connectors',
 'workcell.integrations.types',
 'workcell.templates.runtime.python3.8',
 'workcell.templates.scaffold.python3.8',
 'workcell.ui']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.6,<0.5.0',
 'docker>=6.0.1,<7.0.0',
 'fastapi>=0.85.1,<0.86.0',
 'loguru>=0.6.0,<0.7.0',
 'mangum>=0.17.0,<0.18.0',
 'pandas>=1.5.2,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'streamlit>=1.15.2,<2.0.0',
 'typer>=0.3.1,<0.4.0',
 'uvicorn>=0.18.3,<0.19.0']

entry_points = \
{'console_scripts': ['workcell = workcell.cli:cli']}

setup_kwargs = {
    'name': 'workcell',
    'version': '0.0.10',
    'description': 'Turn python function into microservice.',
    'long_description': '<!-- markdownlint-disable MD033 MD041 -->\n<h1 align="center">\n    Workcell\n</h1>\n\n<p align="center">\n    <strong>Instantly turn your Python function into production-ready microservice.</strong>\n</p>\n\n<p align="center">\n    <a href="https://pypi.org/project/workcell/" title="PyPi Version"><img src="https://img.shields.io/pypi/v/workcell?color=green&style=flat"></a>\n    <a href="https://pypi.org/project/workcell/" title="Python Version"><img src="https://img.shields.io/badge/Python-3.8%2B-blue&style=flat"></a>\n    <a href="https://github.com/weanalyze/orpyter/blob/main/LICENSE" title="Project License"><img src="https://img.shields.io/badge/License-Apache2.0-blue.svg"></a>\n</p>\n\n<p align="center">\n  <a href="#getting-started">Getting Started</a> •\n  <a href="#license">License</a> •\n  <a href="https://github.com/weanalyze/orpyter/releases">Changelog</a>\n</p>\n\nInstantly turn your Python function into production-ready microservice, with lightweight UI to interact with. Use / Share / Publish / Collaborate with your team. \n\n<sup>Pre-alpha Version: Not feature-complete and only suggested for experimental usage.</sup>\n\n<img align="center" style="width: 100%" src="https://github.com/weanalyze/weanalyze-resources/blob/main/assets/workcell_intro.png?raw=true"/>\n\n---\n\n## Highlights\n\n- 🪄&nbsp; Turn functions into production-ready services within seconds.\n- 🔌&nbsp; Auto-generated HTTP API based on FastAPI.\n- 📦&nbsp; Deploy microservice into weanalye FaaS cloud.\n- 🧩&nbsp; Reuse pre-defined templates & combine with existing components.\n- 📈&nbsp; Instantly deploy and scale for production usage.\n\n## Getting Started\n\n### Installation\n\n> _Requirements: Python 3.8+._\n\n```bash\npip install workcell\n```\n\n### Usage\n\n1. A simple orpyter-compatible function could look like this:\n\n    ```python\n    from pydantic import BaseModel\n\n    class Input(BaseModel):\n        message: str\n\n    class Output(BaseModel):\n        message: str\n\n    def hello_workcell(input: Input) -> Output:\n        """Returns the `message` of the input data."""\n        return Output(message=input.message)\n    ```\n\n    _💡 A workcell-compatible function is required to have an `input` parameter and return value based on [Pydantic models](https://pydantic-docs.helpmanual.io/). The input and output models are specified via [type hints](https://docs.python.org/3/library/typing.html)._\n\n2. Copy this code to a file named `app.py`, put into a folder, e.g. `hello_workcell`\n\n3. Run the HTTP API server from command-line:\n\n    ```bash\n    cd hello_workcell\n    workcell serve app:hello_workcell\n    ```\n    _In the output, there\'s a line that shows where your API is being served, on your local machine._\n\n4. Run the Streamlit based UI server from command-line:\n\n    ```bash\n    workcell serve-ui app:hello_workcell\n    ```\n    _In the output, there\'s a line that shows where your UI is being served, on your local machine._\n\n5. Deploy the service into weanalyze cloud from command-line:\n\n    ### requirements\n\n    - [Docker](https://docker.com/) installed\n    - [Dockerhub](https://hub.docker.com/) account\n    - [Weanalyze](https://weanalyze.co) account\n\n    You need both [dockerhub](https://hub.docker.com/) and [weanalyze](https://weanalyze.co) account to deploy your function.\n\n    Set environment variable `DOCKERHUB_USERNAME` as your dockerhub username:\n\n    ```bash\n    export DOCKERHUB_USERNAME={YOUR_DOCKERHUB_USERNAME}\n    ```\n\n    or save it into `.env` under your project folder. Your project dir may seems like this:\n\n    ```bash\n    hello_workcell\n    ├── .env\n    ├── app.py\n    └── requirements.txt    \n    ```\n\n    ### usage\n\n    Let\'s deploy your function on weanalyze cloud! \n\n    First, login on weanalyze cloud:\n    \n    ```bash\n    # login on weanalyze cloud\n    workcell login -u {WEANALYZE_USERNAME}    \n    ```\n\n    In your project folder:\n\n    ```bash\n    # 1-click deploy!\n    workcell up app:hello_workcell\n    ```\n    _In the output, there\'s a line that shows where your serverless funtion is being served, on weanalyze cloud._\n\n    If you want to deploy function in multiple steps:\n    \n    ```bash\n    workcell build app:hello_workcell\n    workcell push\n    ```\n    _Build workcell into docker image, then push to dockerhub._\n\n    ```bash\n    workcell deploy\n    ```\n    _Deploy builded docker image on weanalyze cloud._\n\n\n5. Find out more usage information and get inspired by our [examples](https://github.com/weanalyze/workcell/tree/main/examples).\n\n## License\n\nApache-2.0 License.\n',
    'author': 'jiandong',
    'author_email': 'jiandong@weanalyze.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
