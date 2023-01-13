# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_jupyter_plugin']

package_data = \
{'': ['*'], 'poetry_jupyter_plugin': ['assets/*']}

install_requires = \
['asset>=0.6.13,<0.7.0', 'jupyter-client>=7.4.8,<8.0.0', 'poetry>=1.3.2,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['jupyter-command = '
                               'poetry_jupyter_plugin.plugin:JupyterKernelPlugin']}

setup_kwargs = {
    'name': 'poetry-jupyter-plugin',
    'version': '0.1.3',
    'description': 'Poetry plugin to manage Jupyter kernels',
    'long_description': '# poetry-jupyter-plugin\n\n## overview\n\nThis is a really simple plugin to allow you to install your\n[Poetry](https://python-poetry.org) virtual environment as a\n[Jupyter](https://jupyter.org) kernel. You may wish to do this to keep your\ndependencies locked down for reproducible notebooks, or to set up a single\n"data science" notebook for one-off calculations without fiddling about with\ninstalling packages globally or dealing with `ipykernel` directly.\n\n## getting started\n\nInstall the plugin with:\n\n```sh\n$ poetry self add poetry-jupyter-plugin\n```\n\nThen, from within your poetry project:\n\n```sh\n$ poetry install ipykernel -G dev\n$ poetry jupyter install\n```\n\nRemove the kernelspec with:\n\n```sh\n$ poetry jupyter remove\n```\n\n### configuration\n\nBy default, the installed kernel will use the name of the project and a default\nPoetry icon. To configure these options, add this block to your `pyproject.toml`:\n\n```toml\n[tool.jupyter.kernel]\nname = "my-cool-kernel"\ndisplay = "My cool kernel"\nicon = "/path/to/icon.png"\n```\n\n## prior art\n\nThere are other projects in this space, notably Pathbird\'s [`poetry-kernel`].\n`poetry-kernel` installs a single kernelspec globally which then patches the\nvirtualenv based on the specific project folder that you\'re running Jupyter in.\nThis has some pros and cons over this project.\n\nPros:\n\n1. Single kernelspec, avoiding polluting the kernelspec list with lots of specs.\n2. Easy context switching between projects.\n\nCons:\n\n1. Notebooks have to be in the same folder (or a subfolder from) as the\n   `pyproject.toml` folder.\n2. Requires forwarding signals from the launcher into Jupyter, introducing a\n   layer of complexity and is brittle to changes in Jupyter protocol/underlying\n   OS.\n3. Implicit dependency on `ipykernel`, and may fail to start without it.\n\nIn contrast, this project installs one kernelspec per virtualenv and leaves it\nup to Jupyter to launch the kernel normally without interception. This design\ndecision also allows multiple projects to be based out of one kernel.\nAdditionally, the tool checks for the existence of `ipykernel` to make sure\nthat the kernel can be installed properly.\n\n## who?\n\nThis was written by [patrick kage](//ka.ge).\n',
    'author': 'Patrick Kage',
    'author_email': 'patrick.r.kage@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pkage/poetry-jupyter-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
