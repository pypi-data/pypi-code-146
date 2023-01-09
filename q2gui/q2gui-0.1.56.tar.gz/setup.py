# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['q2gui', 'q2gui.pyqt6', 'q2gui.pyqt6.widgets']

package_data = \
{'': ['*']}

install_requires = \
['PyQt6-QScintilla>=2.13.3,<3.0.0', 'PyQt6>=6.3.0,<7.0.0', 'q2db>=0.1.10']

setup_kwargs = {
    'name': 'q2gui',
    'version': '0.1.56',
    'description': 'Python GUI toolkit',
    'long_description': '# The light Python GUI builder (currently based on PyQt6)\n\n# How to start \n## With docker && x11:\n```bash\ngit clone https://github.com/AndreiPuchko/q2gui.git\n#                      sudo if necessary \ncd q2gui/docker-x11 && ./build_and_run_menu.sh\n```\n## With PyPI package:\n```bash\npoetry new project_01 && cd project_01 && poetry shell\npoetry add q2gui\ncd project_01\npython -m q2gui > example_app.py && python example_app.py\n```\n## Explore sources:\n```bash\ngit clone https://github.com/AndreiPuchko/q2gui.git\ncd q2gui\npip3 install poetry\npoetry shell\npoetry install\npython3 demo/demo_00.py     # All demo launcher\npython3 demo/demo_01.py     # basic: main menu, form & widgets\npython3 demo/demo_02.py     # forms and forms in form\npython3 demo/demo_03.py     # grid form (CSV data), automatic creation of forms based on data\npython3 demo/demo_04.py     # progressbar, data loading, sorting and filtering\npython3 demo/demo_05.py     # nonmodal form\npython3 demo/demo_06.py     # code editor\npython3 demo/demo_07.py     # database app (4 tables, mock data loading) - requires a q2db package\npython3 demo/demo_08.py     # database app, requires a q2db package, autoschema\n```\n\n## demo/demo_07.py screenshot\n=======\n![Alt text](https://andreipuchko.github.io/q2gui/screenshot.png)\n# Build standalone executable \n(The resulting executable file will appear in the folder  dist/)\n### One file\n```bash\npyinstaller -F demo/demo.py\n```\n\n### One directory\n```bash\npyinstaller -D demo/demo.py\n```\n',
    'author': 'Andrei Puchko',
    'author_email': 'andrei.puchko@gmx.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
