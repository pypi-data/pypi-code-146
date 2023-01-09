# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['q2rad']

package_data = \
{'': ['*']}

install_requires = \
['q2db>=0.1.9,<0.2.0', 'q2gui>=0.1.36,<0.2.0', 'q2report>=0.1.16,<0.2.0']

entry_points = \
{'console_scripts': ['q2rad = q2rad.q2rad:main']}

setup_kwargs = {
    'name': 'q2rad',
    'version': '0.1.90',
    'description': 'RAD - database, GUI, reports',
    'long_description': '# The RAD (rapid application development) system. \n\n**(code less, make more)**  \n**Based on:**  \n    q2db        (https://pypi.org/project/q2db)  \n    q2gui       (https://pypi.org/project/q2gui)  \n    q2report    (https://pypi.org/project/q2report)  \n\n## [Read the docs](docs/index.md) \n## Install & run\n**Linux**\n```bash\nmkdir q2rad && \\\n    cd q2rad && \\\n    python3 -m pip install --upgrade pip && \\\n    python3 -m venv q2rad && \\\n    source q2rad/bin/activate && \\\n    python3 -m pip install --upgrade q2rad && \\\n    q2rad\n```\n**Windows**\n```bash\nmkdir q2rad && \\\n    cd q2rad && \\\n    py -m pip install --upgrade pip && \\\n    py -m venv q2rad && \\\n    call q2rad/scripts/activate && \\\n    pip install --upgrade q2rad  && \\\n    q2rad\n```\n**Mac**\n```bash\nmkdir q2rad && \\\n    cd q2rad && \\\n    python3 -m pip install --upgrade pip && \\\n    python3 -m venv q2rad && \\\n    source q2rad/bin/activate && \\\n    python3 -m pip install --upgrade q2rad && \\\n    q2rad\n```\n**Docker**\n```bash\ncurl -s https://raw.githubusercontent.com/AndreiPuchko/q2rad/main/docker-x11/dockerfile > dockerfile && \\\n    mkdir -p q2rad_storage/Desktop && \\\n    chmod -R 777 q2rad_storage && \\\n    sudo docker build -t q2rad . && \\\n    sudo docker run -it \\\n        -v /tmp/.X11-unix:/tmp/.X11-unix \\\n        -v $(pwd)/q2rad_storage:/home/q2rad \\\n        -e DISPLAY=$DISPLAY \\\n        -u q2rad q2rad python3 -m q2rad\n\n```\n## Concept:\nApplication as a database\n```python\nForms:        #  may have main menu (menubar) definitions\n              #  may be linked to database table\n    \n    Lines:    #  form fields(type of data and type of form control) and \n              #  layout definitions\n              #  when form is linked to database - database columns definitions\n    \n    Actions:  #  applies for database linked forms\n              #  may be standard CRUD-action \n              #  or \n              #  run a script (run reports, forms and etc)\n              #  or\n              #  may have linked subforms (one-to-many)\n\nModules:      #  python scripts\n\nQueries:      #  query development and debugging tool\n\nReports:      #  multiformat (HTML, DOCX, XLSX) reporting tool \n```\n',
    'author': 'Andrei Puchko',
    'author_email': 'andrei.puchko@gmx.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
