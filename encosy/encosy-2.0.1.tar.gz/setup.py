# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['encosy', 'encosy.storage']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'encosy',
    'version': '2.0.1',
    'description': 'ECS python implementation',
    'long_description': '# encosy\n## [Docs](https://cruxyu.github.io/encosy/)\n\n## Installation\n\n### Using pip\nReleases of `encosy` can be installed using pip::\n\n    $ pip install encosy\n\nSource releases and any binaries can be downloaded from the PyPI link.\n\n    https://pypi.org/project/encosy/\n\n\n### Using git and poetry\nFor poetry guide follow [this link](https://python-poetry.org/docs/)::\n    \n    git clone https://github.com/Cruxyu/encosy.git\n    poetry install\n\n### Profiling\n#### CPU\nTo create a profile.prof\n\n    from file_with_app import app\n    import cProfile\n    import pstats\n    \n    \n    def main():\n        with cProfile.Profile() as pr:\n            app()\n        stats = pstats.Stats(pr)\n        stats.sort_stats(pstats.SortKey.TIME)\n        # stats.print_stats()\n        stats.dump_stats("app.prof")\n    \n    \n    if __name__ == "__main__":\n        main()\n\nTo see viz of a profile\n\n    poetry run python -m snakeviz app.prof\n\n#### Memory\nTo test memory run\n\n    mprof run app.py  \n\nTo see the results run\n    \n    mprof plot\n\n',
    'author': 'Cruxyu',
    'author_email': 'a.kovalenko.ai@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
