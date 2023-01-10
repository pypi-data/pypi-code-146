# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_aiohttp']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'aiohttp[speedups]>=3.8.1,<4.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'ujson>=5.7.0,<6.0.0']

setup_kwargs = {
    'name': 'pydantic-aiohttp',
    'version': '0.6.0',
    'description': 'Simple HTTP Client based on aiohttp with integration of pydantic',
    'long_description': '# pydantic_aiohttp - Symbiosis of [Pydantic](https://github.com/samuelcolvin/pydantic) and [Aiohttp](https://github.com/aio-libs/aiohttp)\n\n[![PyPI version shields.io](https://img.shields.io/pypi/v/pydantic_aiohttp.svg)](https://pypi.python.org/pypi/pydantic_aiohttp/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pydantic_aiohttp.svg)](https://pypi.python.org/pypi/pydantic_aiohttp/)\n[![PyPI license](https://img.shields.io/pypi/l/pydantic_aiohttp.svg)](https://pypi.python.org/pypi/pydantic_aiohttp/)\n\nThis repository provides simple HTTP Client based on aiohttp with integration of pydantic\n\n## Examples\n\n### Basic example\n\n```python\nimport asyncio\n\nimport pydantic\n\nfrom pydantic_aiohttp import Client\nfrom pydantic_aiohttp.responses import (\n    JSONResponseClass,\n    PlainTextResponseClass,\n    PydanticModelResponseClass\n)\n\n\nclass Todo(pydantic.BaseModel):\n    userId: int\n    id: int\n    title: str\n    completed: bool\n\n\nasync def main():\n    client = Client(\'https://jsonplaceholder.typicode.com\')\n\n    async with client:\n        # Text response\n        todo = await client.get(\'/todos/1\', response_class=PlainTextResponseClass)\n        print(isinstance(todo, str))  # True\n\n        # JSON Response\n        todo = await client.get(\'/todos/1\', response_class=JSONResponseClass)\n        print(isinstance(todo, dict))  # True\n        # You can achieve the same result if you know exact shape of response, dict for example\n        todo = await client.get(\'/todos/1\', response_class=PydanticModelResponseClass, response_model=dict)\n        print(isinstance(todo, dict))  # True\n\n        # Deserialization in pydantic model\n        todo = await client.get(\'/todos/1\', response_class=PydanticModelResponseClass, response_model=Todo)\n        print(isinstance(todo, Todo))  # True\n\n        # PydanticModelResponseClass is used by default, so you can omit it\n        todo = await client.get(\'/todos/1\', response_model=Todo)\n        print(isinstance(todo, Todo))  # True\n\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n\n\n```\n\n### Explicitly close connection\n\n```python\nimport asyncio\n\nimport pydantic\n\nfrom pydantic_aiohttp import Client\n\nclass Todo(pydantic.BaseModel):\n    userId: int\n    id: int\n    title: str\n    completed: bool\n\n\nasync def main():\n    client = Client(\'https://jsonplaceholder.typicode.com\')\n\n    try:\n        await client.get(\'/todos/1\', response_model=Todo)\n    finally:\n        # Don\'t forget to close client session after use\n        await client.close()\n\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n\n```\n\n### Downloading files\n\n```python\nimport asyncio\nimport uuid\n\nfrom pydantic_aiohttp import Client\n\n\nasync def main():\n    client = Client(\'https://source.unsplash.com\')\n\n    async with client:\n        filepath = await client.download_file("/random", filepath=f"random_{uuid.uuid4()}.jpg")\n        print(filepath)\n\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n\n```\n\n### Handling errors parsed as pydantic models\n\n```python\nimport http\nimport asyncio\n\nimport pydantic\n\nimport pydantic_aiohttp\nfrom pydantic_aiohttp import Client\n\n\nclass FastAPIValidationError(pydantic.BaseModel):\n    loc: list[str]\n    msg: str\n    type: str\n\n\nclass FastAPIUnprocessableEntityError(pydantic.BaseModel):\n    detail: list[FastAPIValidationError]\n\n\nclass User(pydantic.BaseModel):\n    id: str\n    email: str\n    first_name: str\n    last_name: str\n    is_admin: bool\n\n\nasync def main():\n    client = Client(\n        "https://fastapi.example.com",\n        error_response_models={\n            http.HTTPStatus.UNPROCESSABLE_ENTITY: FastAPIUnprocessableEntityError\n        }\n    )\n\n    try:\n        # Imagine, that "email" field is required for this route\n        await client.post(\n            "/users",\n            body={\n                "first_name": "John",\n                "last_name": "Doe"\n            },\n            response_model=User\n        )\n    except pydantic_aiohttp.HTTPUnprocessableEntity as e:\n        # response field of exception now contain parsed pydantic model entity \n        print(e.response.detail[0].json(indent=4))\n        # >>>\n        # {\n        #     "loc": [\n        #         "body",\n        #         "email"\n        #     ],\n        #     "msg": "field required",\n        #     "type": "value_error.missing"\n        # }\n    finally:\n        await client.close()\n\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n\n```\n\n## LICENSE\n\nThis project is licensed under the terms of the [MIT](https://github.com/pylakey/aiotdlib/blob/master/LICENSE) license.\n',
    'author': 'pylakey',
    'author_email': 'pylakey@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pylakey/pydantic_aiohttp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
