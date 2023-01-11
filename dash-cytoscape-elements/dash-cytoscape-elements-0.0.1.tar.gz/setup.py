# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dash_cytoscape_elements']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'dash-cytoscape-elements',
    'version': '0.0.1',
    'description': 'Python object for dash-cytoscape elements',
    'long_description': '# dash-cytoscape-elements\n[![test](https://github.com/minefuto/dash-cytoscape-elements/actions/workflows/test.yml/badge.svg)](https://github.com/minefuto/dash-cytoscape-elements/actions/workflows/test.yml)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dash-cytoscape-elements)\n![PyPI](https://img.shields.io/pypi/v/dash-cytoscape-elements)\n![GitHub](https://img.shields.io/github/license/minefuto/dash-cytoscape-elements)\n\nThis is a Python object for [Dash Cytoscape](https://github.com/plotly/dash-cytoscape) Elements.\n\n## Features\n- Add/Remove/Get/Filter Element(Node/Edge) on Python object.\n- Convert Python object from/to Dash Cytoscape format \n- Convert Python object from/to json(Cytoscape.js format)\n\n## Install\n```\npip install dash-cytoscape-elements\n```\n\n## Usage\nExample1: Create Elements object & using on Dash Cytoscape  \n```python\nimport dash\nimport dash_cytoscape as cyto\nfrom dash import html\nfrom dash_cytoscape_elements import Elements\n\nelements = Elements()\nelements.add(id="one", label="Node 1", x=50, y=50)\nelements.add(id="two", label="Node 2", x=200, y=200)\nelements.add(source="one", target="two", label="Node 1 to 2")\n\napp = dash.Dash(__name__)\napp.layout = html.Div([\n    cyto.Cytoscape(\n        id=\'cytoscape\',\n        elements=elements.to_dash(),\n        layout={\'name\': \'preset\'}\n    )\n])\n\nif __name__ == \'__main__\':\n    app.run_server(debug=True)\n```\nExample2: Edit json file of Elements.\n```python\nfrom dash_cytoscape_elements import Elements\n\ne = Elements.from_file("elements.json")\ne.remove(id="node2")\ne.remove(source="node1", target="node2")\n\nwith open("elements.json", mode=\'w\') as f:\n    f.write(e.to_json())\n```\n\nPlease see the [Documentation](https://minefuto.github.io/dash-cytoscape-elements/) for details.\n',
    'author': 'minefuto',
    'author_email': 'minefuto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/minefuto/dash-cytoscape-elements',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
