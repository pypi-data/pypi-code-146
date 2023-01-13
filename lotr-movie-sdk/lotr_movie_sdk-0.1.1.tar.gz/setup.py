# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lotr_movie_sdk']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

extras_require = \
{'docs': ['Sphinx==4.2.0',
          'sphinx-rtd-theme==1.0.0',
          'sphinxcontrib-napoleon==0.7']}

setup_kwargs = {
    'name': 'lotr-movie-sdk',
    'version': '0.1.1',
    'description': 'Lord Of TheRings Movie SDK - Test for LibLab',
    'long_description': '# lotr_movie_sdk package\n\n## Submodules\n\n## lotr_movie_sdk.movie module\n\nLord Of The Rings Movie SDK, based on the api exposed by: [https://the-one-api.dev/](https://the-one-api.dev/).\n\n\n### _class_ lotr_movie_sdk.movie.Movie(key, url=\'https://the-one-api.dev/v2\')\nBases: `object`\n\n\n#### \\__init__(key, url=\'https://the-one-api.dev/v2\')\nInitialization of the movie SDK that sets the api key & URL of the endpoint.\n\nArgs:\n\n    key (str): String representing the api key.\n    url (str): Optional parameter - a string representing the base URL for the API endpoint\n\n    > (defaults to [https://the-one-api.dev/v2](https://the-one-api.dev/v2)).\n\nExamples:\n\n    ```python\n    >>> hello("Roman")\n    \'Hello Roman!\'\n    ```\n\n\n#### get(id)\nGet the metadata of a movie with the specified id.\n\nArgs:\n\n    id (str): String representing the movie id.\n\nReturns:\n\n    Dict: movie details\n\nExamples:\n\n    ```python\n    >>> m.get("345t453t3")\n    \'{"_id":"345t453t3","name":"movie1",....}\'\n    ```\n\n\n* **Return type**\n\n    `dict`\n\n\n\n#### list()\nGet list of all the movies with their metadata.\n\nReturns:\n\n    List: list of movies with their metadata\n\nExamples:\n\n    ```python\n    >>> m.list()\n    \'[{"_id":"45t5t45t454",\'name\':\'movie1\',....},...]\'\n    ```\n\n\n* **Return type**\n\n    `list`\n\n\n\n#### quotes(id)\nList all the quotes of a movie with the specified id.\n\nArgs:\n\n    id (str): String representing the movie id.\n\nReturns:\n\n    List: list of movie quotes\n\nExamples:\n\n    ```python\n    >>> m.quotes("345t453t3")\n    \'[{"_id":"34r43r43r","quote":"Hello world"},....]\'\n    ```\n\n\n* **Return type**\n\n    `list`\n\n\n## Module contents\n\nLord Of TheRings Movie SDK - Test for LibLab\n\n\n### lotr_movie_sdk.get_version()\n\n* **Return type**\n\n    `str`\n',
    'author': 'sciffer',
    'author_email': 'shaly.c@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sciffer/lotr-movie-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
