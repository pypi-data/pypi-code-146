# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynamicadaptor']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'dynamicadaptor',
    'version': '0.1.7',
    'description': '',
    'long_description': '\n# DynamicAdaptor\n-------------\n\n用于将bilibili的grpc动态和web动态转换成特定的数据类型\n\n\n### 原理说明\n将grpc数据转换成json数据，之后使用pydantic进行信息摘要。\nweb端的json数据同理\n\n\n### 下载安装\n``` xml\npip install dynamicadaptor\n```\n\n### 使用方法\n\n```python\n\nfrom google.protobuf.json_format import MessageToDict\nfrom dynamicadaptor.DynamicConversion import formate_message\nfrom bilirpc.api import get_dy_detail\nimport asyncio\nimport httpx\n\n\n# 如果数据是grpc返回的数据，则需要转换成json数据\nasync def sample1():\n    dynamic_grpc = await get_dy_detail("746530608345251842")\n    dynamic: dict = MessageToDict(dynamic_grpc[0])\n    dynamic_formate = formate_message("grpc", dynamic)\n    print(dynamic_formate)\n\n\nasyncio.run(sample1())\n\n\n# 如果是web返回的数据\nasync def sample2():\n    url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/detail?timezone_offset=-480&id=746530608345251842"\n    headers = {\n        "Referer": "https://t.bilibili.com/746530608345251842"\n    }\n    result = httpx.get(url, headers=headers).json()\n    dynamic_formate = formate_message("web", result["data"]["item"])\n    print(dynamic_formate)\n\n\nasyncio.run(sample2())\n\n\n\n\n```\n\n\n\n## License\nGPL\n',
    'author': 'DMC',
    'author_email': 'lzxder@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
