# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modbus_connect']

package_data = \
{'': ['*']}

install_requires = \
['pymodbus>=3.0.2,<4.0.0']

setup_kwargs = {
    'name': 'modbus-connect',
    'version': '0.1.2',
    'description': 'Modbus TCP data acquisition library',
    'long_description': '# Modbus Connect package for Python\n\n<a href="https://angelfernandezsobrino.github.io/modbus-connect/reports/tests/3.11.html" alt="Tests">\n    <img src="https://angelfernandezsobrino.github.io/modbus-connect/badges/tests/3.11.svg">\n</a>\n<a href="https://angelfernandezsobrino.github.io/modbus-connect/reports/coverage/3.11/index.html" alt="Tests">\n    <img src="https://angelfernandezsobrino.github.io/modbus-connect/badges/coverage/3.11.svg">\n</a>\n\n\nModbus Connect is a Python package that provides a configurable Modbus TCP data adquisition library from Modbus TCP devices. It is designed to be used as a library for a data acquisition application, managing the connection to the devices and the data exchange with them. The data is returned in a format that can be easily used for sending to a database or MQTT broker.\n\nThe Modbus data table can be supplied as a csv file or as a Python dictionary. A dictionary is used to configure the Modbus Gateway. The dictionary can be created manually or by using the importer module from a csv file.\n\nIt is based on the [PyModbus](https://github.com/riptideio/pymodbus) for the Modbus TCP communication.\n\nThe [modbus-mqtt-digital-twin]() package provides a data acquisition application that uses the Modbus Gateway library. (Under development)\n\n\n## Installation\n\nThe package can be installed from PyPI:\n\n```bash\npip install modbus\n```\n\n## Usage\n\nFor a complete example of the usage of the package, check the examples folder.\n\nHere is a simple example of the usage of the package:\n\n```python\nfrom modbus_gateway import ModbusGateway\n\n# Create a dictionary with the configuration of the Modbus Gateway\n\nconfig = [\n    {\n        "name": "var1",\n        "address": 0,\n        "memory_bank": utils.MemoryBanks.HOLDING_REGISTERS,\n        "datatype": "float32",\n    },\n    {\n        "name": "var2",\n        "address": 2,\n        "memory_bank": utils.MemoryBanks.HOLDING_REGISTERS,\n        "datatype": "float32",\n    },\n]\n\ngateway = ModbusGateway(\n    host=<host>,\n    port=<port>,\n    tags_list=config,\n)\n\n# Read the values from the modbus server\n\nvalues = gateway.read_tags()\nprint(values)\n```\n\nThis behaviour can be easly used for continuous data adquisition using rocktry or any other scheduler and fastly deploied using docker.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## Authors\n\n-   **Ángel Fernández Sobrino** - [AngelFernandezSobrino](https://github.com/AngelFernandezSobrino)',
    'author': 'Ángel Fernández Sobrino',
    'author_email': 'fernandezsobrinoangel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
