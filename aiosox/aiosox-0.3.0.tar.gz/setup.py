# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiosox',
 'aiosox.asyncapi',
 'aiosox.kafka',
 'aiosox.ponicode',
 'aiosox.sio',
 'aiosox.sio.ponicode']

package_data = \
{'': ['*']}

install_requires = \
['aiokafka>=0.8.0,<0.9.0',
 'anyio[trio]>=3.6.2,<4.0.0',
 'fastapi>=0.88.0,<0.89.0',
 'mkdocs-material>=9.0.2,<10.0.0',
 'mkdocs>=1.4.2,<2.0.0',
 'orjson>=3.8.3,<4.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'python-socketio>=5.7.2,<6.0.0',
 'uvicorn[standard]>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'aiosox',
    'version': '0.3.0',
    'description': '⛓️ Combination of asyncapi(documentation) & socketio pub/sub using aiokafka as the client manager  multinode backend services',
    'long_description': '![Sample image](https://gitlab.com/uploads/-/system/project/avatar/42327849/a5e01db694b47cd07018813ce821a4e1.png?width=64)\n\n\naiosox: <a href="https://gitlab.com/arieutils/aiosox">repo link </a>\n=======================================\nQuick example\n-----------\n\ncan be installed using pip/poetry:\n\n    poetry shell\n     \n    poetry run uvicorn example:app --port=8001\n    \n```python\nfrom typing import List\n\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel\n\nfrom aiosox import SioAuth, SioNamespace, SocketIoServer\n\n\ndef get_app():\n    applitcation = FastAPI(title="tester")\n    return applitcation\n\n\napp = get_app()\n\nsio_server: SocketIoServer = SocketIoServer(app=app, kafka_url="localhost:29092")\nuser_namespapce: SioNamespace = SioNamespace("/user", socket_io_server=sio_server)\nsio_server._sio.register_namespace(user_namespapce)\n\n\n@app.on_event("startup")\nasync def on_start():\n    await sio_server.start()\n\n\n@app.on_event("shutdown")\nasync def on_shutdown():\n    await sio_server.shutdown()\n\n\nclass UserY(BaseModel):\n    name: str\n\n\nclass UserT(BaseModel):\n    name: str\n    what: List[UserY]\n\n\nclass OfferT(BaseModel):\n    title: str\n\n\non_failed_emmiter = user_namespapce.create_emitter("failed", model=OfferT | UserT)\n\n\n@user_namespapce.on(\n    "submit",\n    description="when user submits a form",\n    payload_model=UserT | UserY,\n    response_model=List[UserT],\n    auth=SioAuth.jwt,\n)\nasync def on_submit(sid, data):\n    print(\n        sid,\n        data,\n    )\n\n```',
    'author': 'Arie',
    'author_email': 'ariesorkin3@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/arieutils/aiosox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.11.1',
}


setup(**setup_kwargs)
