# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['i18n']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.89.0,<0.90.0',
 'pydantic[dotenv]>=1.10.4,<2.0.0',
 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'fastapi-i18n',
    'version': '0.1.2',
    'description': 'Fastapi i18n',
    'long_description': '# README\n\n## 1. Quick start\n\nInstall the package:\n\n```shell\npip install fastapi-i18n\n```\n\nUsage in your project:\n\n```python\nimport i18n\nfrom fastapi import FastAPI, Depends\n\napp = FastAPI()\n\n\n@app.on_event("startup")\nasync def startup():\n    await i18n.init()\n\n@app.get(\'/\')\nasync def root(translator: i18n.Translator = Depends(i18n.Translator)):\n    return {"message": translator.t(\'hello.world\')}\n```\n',
    'author': 'tricker.pan',
    'author_email': 'tricker.pan@gmail.com',
    'maintainer': 'tricker.pan',
    'maintainer_email': 'tricker.pan@gmail.com',
    'url': 'https://github.com/TrickerPan/fastapi-i18n',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
