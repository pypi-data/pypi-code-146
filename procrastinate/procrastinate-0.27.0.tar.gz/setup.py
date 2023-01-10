# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['procrastinate',
 'procrastinate.contrib',
 'procrastinate.contrib.django',
 'procrastinate.contrib.sqlalchemy',
 'procrastinate.sql',
 'procrastinate.sql.migrations']

package_data = \
{'': ['*'], 'procrastinate.sql': ['future_migrations/*']}

install_requires = \
['aiopg', 'attrs', 'click', 'croniter', 'psycopg2-binary', 'python-dateutil']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata', 'typing-extensions'],
 ':python_version < "3.9"': ['importlib-resources>=1.4'],
 'django': ['django>=2.2'],
 'sqlalchemy': ['sqlalchemy>=1.4,<2.0']}

entry_points = \
{'console_scripts': ['procrastinate = procrastinate.cli:main']}

setup_kwargs = {
    'name': 'procrastinate',
    'version': '0.27.0',
    'description': 'Postgres-based distributed task processing library',
    'long_description': 'Procrastinate: PostgreSQL-based Task Queue for Python\n=====================================================\n\n.. image:: https://img.shields.io/pypi/v/procrastinate?logo=pypi&logoColor=white\n    :target: https://pypi.org/pypi/procrastinate\n    :alt: Deployed to PyPI\n\n.. image:: https://img.shields.io/pypi/pyversions/procrastinate?logo=pypi&logoColor=white\n    :target: https://pypi.org/pypi/procrastinate\n    :alt: Deployed to PyPI\n\n.. image:: https://img.shields.io/github/stars/procrastinate-org/procrastinate?logo=github\n    :target: https://github.com/procrastinate-org/procrastinate/\n    :alt: GitHub Repository\n\n.. image:: https://img.shields.io/github/actions/workflow/status/procrastinate-org/procrastinate/ci.yml?logo=github&branch=main\n    :target: https://github.com/procrastinate-org/procrastinate/actions?workflow=CI\n    :alt: Continuous Integration\n\n.. image:: https://img.shields.io/readthedocs/procrastinate?logo=read-the-docs&logoColor=white\n    :target: http://procrastinate.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation\n\n.. image:: https://img.shields.io/endpoint?logo=codecov&logoColor=white&url=https://raw.githubusercontent.com/wiki/procrastinate-org/procrastinate/python-coverage-comment-action-badge.json\n    :target: https://github.com/marketplace/actions/python-coverage-comment\n    :alt: Coverage\n\n.. image:: https://img.shields.io/github/license/procrastinate-org/procrastinate?logo=open-source-initiative&logoColor=white\n    :target: https://github.com/procrastinate-org/procrastinate/blob/main/LICENSE\n    :alt: MIT License\n\n.. image:: https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg\n    :target: https://github.com/procrastinate-org/procrastinate/blob/main/LICENSE/CODE_OF_CONDUCT.md\n    :alt: Contributor Covenant\n\n\nProcrastinate is an open-source Python 3.7+ distributed task processing\nlibrary, leveraging PostgreSQL to store task definitions, manage locks and\ndispatch tasks. It can be used within both sync and async code.\n\nIn other words, from your main code, you call specific functions (tasks) in a\nspecial way and instead of being run on the spot, they\'re scheduled to\nbe run elsewhere, now or in the future.\n\nHere\'s an example:\n\n.. code-block:: python\n\n    # mycode.py\n    import procrastinate\n\n    # Make an app in your code\n    app = procrastinate.App(connector=procrastinate.AiopgConnector())\n\n    # Then define tasks\n    @app.task(queue="sums")\n    def sum(a, b):\n        with open("myfile", "w") as f:\n            f.write(str(a + b))\n\n    with app.open():\n        # Launch a job\n        sum.defer(a=3, b=5)\n\n        # Somewhere in your program, run a worker (actually, it\'s often a\n        # different program than the one deferring jobs for execution)\n        app.run_worker(queues=["sums"])\n\nThe worker will run the job, which will create a text file\nnamed ``myfile`` with the result of the sum ``3 + 5`` (that\'s ``8``).\n\nSimilarly, from the command line:\n\n.. code-block:: bash\n\n    export PROCRASTINATE_APP="mycode.app"\n\n    # Launch a job\n    procrastinate defer mycode.sum \'{"a": 3, "b": 5}\'\n\n    # Run a worker\n    procrastinate worker -q sums\n\nLastly, you can use Procrastinate asynchronously too:\n\n.. code-block:: python\n\n    import asyncio\n\n    import procrastinate\n\n    # Make an app in your code\n    app = procrastinate.App(connector=procrastinate.AiopgConnector())\n\n    # Define tasks using coroutine functions\n    @app.task(queue="sums")\n    async def sum(a, b):\n        await asyncio.sleep(a + b)\n\n    async with app.open_async():\n        # Launch a job\n        await sum.defer_async(a=3, b=5)\n\n        # Somewhere in your program, run a worker (actually, it\'s often a\n        # different program than the one deferring jobs for execution)\n        await app.run_worker_async(queues=["sums"])\n\nThere are quite a few interesting features that Procrastinate adds to the mix.\nYou can head to the Quickstart section for a general tour or\nto the How-To sections for specific features. The Discussion\nsection should hopefully answer your questions. Otherwise,\nfeel free to open an `issue <https://github.com/procrastinate-org/procrastinate/issues>`_.\n\nThe project is still quite early-stage and will probably evolve.\n\n*Note to my future self: add a quick note here on why this project is named*\n"Procrastinate_".\n\n.. _Procrastinate: https://en.wikipedia.org/wiki/Procrastination\n\n.. Below this line is content specific to the README that will not appear in the doc.\n.. end-of-index-doc\n\nWhere to go from here\n---------------------\n\nThe complete docs_ is probably the best place to learn about the project.\n\nIf you encounter a bug, or want to get in touch, you\'re always welcome to open a\nticket_.\n\n.. _docs: http://procrastinate.readthedocs.io/en/latest\n.. _ticket: https://github.com/procrastinate-org/procrastinate/issues/new\n',
    'author': 'Joachim Jablon',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://procrastinate.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
