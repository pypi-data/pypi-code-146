# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aslabs', 'aslabs.dependencies.fastapi']

package_data = \
{'': ['*']}

install_requires = \
['aslabs-dependencies', 'fastapi>=0.86.0,<0.87.0']

setup_kwargs = {
    'name': 'aslabs-dependencies-fastapi',
    'version': '0.0.7',
    'description': '',
    'long_description': '## ASLabs Dependencies: FastAPI\n\nFastAPI Adapter for the ASLabs Dependencies package.\n\n# How to use it:\n\nIn your `main.py`, add the `Dependencies` additional handler:\n\n```py\nfrom fastapi import FastAPI\n\nfrom aslabs.dependencies.fastapi import Dependencies\n\n\napp = FastAPI()\ndeps = Dependencies(app)    # Add line\n```\n\nIn your various routers, replace `APIRouter` with `DependencyRouter` and use it to register your dependencies:\n\n```py\nfrom aslabs.dependencies.fastapi import DependencyRouter, D\n\n\nrouter = DependencyRouter()\nrouter.register_dependencies(lambda deps: deps.add_direct(MyDependencyClass))      # Register your dependencies here\n```\n\nOnce registered, use the `D` parameter function to request dependencies. Notably, you must specify the type as the parameter for `D` (cannot be infered).\n\n```py\n@router.get("/")\ndef index(dep: MyDependencyClass = D(MyDependencyClass)):\n    return {"Hello": dep.get_world()}\n```\n\nOnce setup, back in your `main.py`, register the router on `deps`, not on `app`. The same parameters can be used as `app.include_router`\n\n```py\ndeps.include_router(router)\n```\n\nYou are now done.\n\n## Adding global dependencies\n\nYou can add dependencies directly to the `deps` object, by calling `register_with`:\n\n```py\ndeps.register_with(lambda deps: deps.add_direct(GlobalDependency))\n```',
    'author': 'Titusz Ban',
    'author_email': 'tituszban@antisociallabs.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
