# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autoserver', 'autoserver.resources']

package_data = \
{'': ['*']}

install_requires = \
['docstring-parser>=0.15,<0.16',
 'fastapi>=0.88.0,<0.89.0',
 'jinja2>=3.1.2,<4.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'uvicorn>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'autoserver',
    'version': '0.1.0',
    'description': '',
    'long_description': '# AutoServer\n\nAutoServer is a python library for making quick web UIs, it was originally made for HackEd 2023. \n\n## Example\n```python\nfrom autoserver import AutoServer\napp = AutoServer()\n\n@app.addfunc\ndef TaxCalc(province: str, cost: float, taxrate: int):\n    """\n    Computes the amount of tax on an item given the tax rate\n    :param province: The name of the province\n    :param cost: The cost of the item expressed in dollars\n    :param taxrate: The tax rate expressed as a percentage\n    :return:\n    """\n    tax = cost * float(taxrate) / 100\n    output = f"The tax in {province} for an item worth ${cost} is {tax}."\n    output += f"The total cost is ${cost + tax}."\n    return output\n\n@app.addfunc\ndef TargetPrice(province: str, targetcost: float, taxrate: int):\n    targetRatio = 1.0 + float(taxrate) / 100\n    output = f"To have a final cost of ${targetcost} in {province},"\n    output += f"the pretax price should be ${targetcost / targetRatio}"\n    return output\n\napp.run()\n```',
    'author': 'JanukanS',
    'author_email': '28988453+JanukanS@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
