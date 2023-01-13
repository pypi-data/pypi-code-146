# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_mlflow']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.73.0', 'mlflow>=1.23.0,<2.0.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'fastapi-mlflow',
    'version': '0.3.2',
    'description': 'Deploy mlflow models as JSON APIs with minimal new code.',
    'long_description': '# fastapi mlflow\n\nDeploy [mlflow](https://www.mlflow.org/) models as JSON APIs using [FastAPI](https://fastapi.tiangolo.com) with minimal new code.\n\n## Installation\n\n```shell\npip install fastapi-mlflow\n```\n\nFor running the app in production, you will also need an ASGI server, such as [Uvicorn](https://www.uvicorn.org) or [Hypercorn](https://gitlab.com/pgjones/hypercorn).\n\n## Install on Apple Silicon (ARM / M1)\n\nIf you experience problems installing on a newer generation Apple silicon based device, [this solution from StackOverflow](https://stackoverflow.com/a/67586301) before retrying install has been found to help.\n\n```shell\nbrew install openblas gfortran\nexport OPENBLAS="$(brew --prefix openblas)"\n```\n\n## License\n\nCopyright © 2022-23 Auto Trader Group plc.\n\n[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0)\n\n## Examples\n\n### Simple\n\n#### Create\n\nCreate a file `main.py` containing:\n\n```python\nfrom fastapi_mlflow.applications import build_app\nfrom mlflow.pyfunc import load_model\n\nmodel = load_model("/Users/me/path/to/local/model")\napp = build_app(model)\n```\n\n#### Run\n\nRun the server with:\n\n```shell\nuvicorn main:app\n```\n\n#### Check\n\nOpen your browser at <http://127.0.0.1:8000/docs>\n\nYou should see the automatically generated docs for your model, and be able to test it out using the `Try it out` button in the UI.\n\n### Serve multiple models\n\nIt should be possible to host multiple models (assuming that they have compatible dependencies...) by leveraging [FastAPIs Sub Applications](https://fastapi.tiangolo.com/advanced/sub-applications/#sub-applications-mounts):\n\n```python\nfrom fastapi import FastAPI\nfrom fastapi_mlflow.applications import build_app\nfrom mlflow.pyfunc import load_model\n\napp = FastAPI()\n\nmodel1 = load_model("/Users/me/path/to/local/model1")\nmodel1_app = build_app(model1)\napp.mount("/model1", model1_app)\n\nmodel2 = load_model("/Users/me/path/to/local/model2")\nmodel2_app = build_app(model2)\napp.mount("/model2", model2_app)\n```\n\n[Run](#run) and [Check](#check) as above.\n\n### Custom routing\n\nIf you want more control over where and how the prediction end-point is mounted in your API, you can build the predictor function directly and use it as you need:\n\n```python\nfrom inspect import signature\n\nfrom fastapi import FastAPI\nfrom fastapi_mlflow.predictors import build_predictor\nfrom mlflow.pyfunc import load_model\n\nmodel = load_model("/Users/me/path/to/local/model")\npredictor = build_predictor(model)\napp = FastAPI()\napp.add_api_route(\n    "/classify",\n    predictor,\n    response_model=signature(predictor).return_annotation,\n    methods=["POST"],\n)\n```\n\n[Run](#run) and [Check](#check) as above.\n',
    'author': 'John Harrison',
    'author_email': 'john.harrison@autotrader.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/autotraderuk/fastapi-mlflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
