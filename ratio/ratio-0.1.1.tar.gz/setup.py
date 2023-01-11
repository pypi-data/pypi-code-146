# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ratio',
 'ratio.application',
 'ratio.console',
 'ratio.database',
 'ratio.database.fields',
 'ratio.database.migrations',
 'ratio.database.models',
 'ratio.database.queries',
 'ratio.database.seeders',
 'ratio.http',
 'ratio.router',
 'ratio.router.resolvers']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'ratio',
    'version': '0.1.1',
    'description': 'The Python Web Framework for developers who like to get shit done',
    'long_description': '<h1 align="center">Ratio</h1>\n<p align="center">\n  The Python web framework for developers who want to get shit done.\n</p>\n<hr />\n<strong>Ratio is currently being developed and all releases in this phase may introduce breaking changes until further notice.\nPlease do not use Ratio in production without carefully considering the consequences.</strong>\n<hr />\n<h2>What is Ratio?</h2>\n<p>\n  Ratio is an asynchronous Python web framework that was built with developer experience in mind. Quick to learn for those\n  who just start out with programming and powerful so that senior developers can build high performance web applications \n  with it. The framework is designed with the Goldilocks principle in mind: just enough. Enough power to run high performance\n  web applications, enough intuitive design, so that developers can easily pick up on the principles.\n</p>\n<p>\n  Ratio borrows ideas from great frameworks, like <a href="https://github.com/django/django" target="_blank">Django</a>, \n  <a href="https://github.com/tiangolo/fastapi" target="_blank">FastAPI</a> and <a href="https://github.com/vercel/next.js" target="_blank">Next.js</a>, \n  and combines them with original concepts to improve the life of a developer when creating web applications for any\n  purpose.\n</p>\n<h2>Ready out of the box</h2>\n<p>\n  Ratio will be shipped with a custom and extensible command line interface, which can be used to perform actions within a\n  project.\n</p>\n<p>\n  This is what we aim Ratio to do:<br>\n  <small>This list is not complete and will be extended after certain releases in the pre-release phase.</small>\n</p>\n\n<ul>\n  <li><strong>File based routing:</strong> Intuitive routing for each incoming request, based on file system.</li>\n  <li><strong>Integrates with databases:</strong> Connect to SQL or SQLite databases from within the application controllers.</li>\n  <li><strong>Write once, use everywhere:</strong> Do not repeat yourself, by defining models, routes and actions you can use them throughout the application.</li>\n  <li><strong>Adheres to standards:</strong> API views are based on <a href="">OpenAPI</a> and the JSON schema standard.</li>\n</ul>\n\n\n<h2>Minimal external dependencies</h2>\n<p>\n  Currently, Ratio only requires the <code>rich</code> package from outside the Python standard library, which is used \n  for rendering beautiful output to the command line. In a future version of Ratio, we might want to remove this direct\n  dependency for users who really want to have no external dependencies.\n</p>',
    'author': 'Job Veldhuis',
    'author_email': 'job@baukefrederik.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
