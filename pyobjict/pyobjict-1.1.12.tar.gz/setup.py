# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['objict']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyobjict',
    'version': '1.1.12',
    'description': 'A Python dict that supports attribute-style access as well as hierarchical keys, JSON serialization, ZIP compression, and more.',
    'long_description': '![](https://github.com/311labs/objict/workflows/tests/badge.svg)\n\n## Turn a dict into an Object or objict!\n\nBased on uberdict(https://github.com/eukaryote/uberdict)\n\n## Installation\n\n```\npip install pyobjict\n```\n\n\n### Some Differences:\n\n * Support for to/from JSON\n * Support for to/from XML\n * Support for to/from ZIP compression (base64)\n * Support to/from file\n * When an attribute is not found it returns None instead of raising an Error\n * Support for .get("a.b.c")\n * Support for delta between to objicts (obj.changes())\n * Will automatically handle key conversion from "a.b.c" to "a -> b -> c" creation\n\n\n## Simple to use!\n\n```python\n>>> from objict import objict\n>>> d1 = objict(name="John", age=24)\n>>> d1\n{\'name\': \'John\', \'age\': 24}\n>>> d1.name\n\'John\'\n>>> d1.age\n24\n>>> d1.gender = "male"\n>>> d1\n{\'name\': \'John\', \'age\': 24, \'gender\': \'male\'}\n>>> d1.gender\n\'male\'\n>>> import datetime\n>>> d1.dob = datetime.datetime(1985, 5, 2)\n>>> d1.dob\ndatetime.datetime(1985, 5, 2, 0, 0)\n>>> d1.toJSON()\n{\'name\': \'John\', \'age\': 24, \'gender\': \'male\', \'dob\': 483865200.0}\n>>> d1.save("test1.json")\n>>> d2 = objict.fromFile("test1.json")\n>>> d2\n{\'name\': \'John\', \'age\': 24, \'gender\': \'male\', \'dob\': 483865200.0}\n>>> d2.toXML()\n\'<name>John</name><age>24</age><gender>male</gender><dob>483865200.0</dob>\'\n>>> d3 = objict(user1=d2)\n>>> d3.user2 = objict(name="Jenny", age=27)\n>>> d3\n{\'user1\': {\'name\': \'John\', \'age\': 24, \'gender\': \'male\', \'dob\': 483865200.0}, \'user2\': {\'name\': \'Jenny\', \'age\': 27}}\n>>> d3.toXML()\n\'<user1><name>John</name><age>24</age><gender>male</gender><dob>483865200.0</dob></user1><user2><name>Jenny</name><age>27</age></user2>\'\n>>> d3.toJSON(True)\n\'{\\n    "user1": {\\n        "name": "John",\\n        "age": 24,\\n        "gender": "male",\\n        "dob": 483865200.0\\n    },\\n    "user2": {\\n        "name": "Jenny",\\n        "age": 27\\n    }\\n}\'\n>>> print(d3.toJSON(True))\n{\n    "user1": {\n        "name": "John",\n        "age": 24,\n        "gender": "male",\n        "dob": 483865200.0\n    },\n    "user2": {\n        "name": "Jenny",\n        "age": 27\n    }\n}\n>>> d3.toZIP()\nb\'x\\x9c\\xab\\xe6R\\x00\\x02\\xa5\\xd2\\xe2\\xd4"C%+\\x85j0\\x17,\\x94\\x97\\x98\\x9b\\n\\x14Q\\xf2\\xca\\xcf\\xc8S\\xd2A\\x88\\\'\\xa6\\x83\\x84\\x8dL\\x90\\x84\\xd2S\\xf3RR\\x8b@\\x8as\\x13sR\\x91\\x15\\xa7\\xe4\\\'\\x01\\x85M,\\x8c-\\xccL\\x8d\\x0c\\x0c\\xf4\\x0c\\xc0R\\xb5:\\x08[\\x8dp\\xd8\\x9a\\x9a\\x97W\\x89\\xc5Zs\\x88\\x01\\\\\\xb5\\x00^\\x1c\\\'I\'\n>>> dz = d3.toZIP()\n>>> d4 = objict.fromZIP(dz)\n>>> d4\n{\'user1\': {\'name\': \'John\', \'age\': 24, \'gender\': \'male\', \'dob\': 483865200.0}, \'user2\': {\'name\': \'Jenny\', \'age\': 27}}\n>>> d5 = d4.copy()\n>>> d5.user1.name\n\'John\'\n>>> d5.user1.name = "Jim"\n>>> d5\n{\'user1\': {\'name\': \'Jim\', \'age\': 24, \'gender\': \'male\', \'dob\': 483865200.0}, \'user2\': {\'name\': \'Jenny\', \'age\': 27}}\n>>> d5.changes(d4)\n{\'user1\': {\'name\': \'John\'}}\n\n```\n\n\n',
    'author': 'Ian Starnes',
    'author_email': 'ians@311labs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
