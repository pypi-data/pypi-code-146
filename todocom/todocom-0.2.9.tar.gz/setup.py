# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['todocom']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['todo = todocom.cli:main']}

setup_kwargs = {
    'name': 'todocom',
    'version': '0.2.9',
    'description': 'CLI to retrieve a list of all TODO comments in the code',
    'long_description': '# todocom (Todo Comments)\nCLI program that retrieves all TODO comments from file(s) and prints them in terminal/shell. It was created in order to automatically update a list of TODO tasks by simply adding "TODO:" comments in the code ([Comments Format](#comments-format)). It also enables prioritization of tasks by using "TODO soon:" or "TODO urgent". \nTo create the TODO list, simply open terminal and run the following command:\n```\ntodo [folder/file]\n```\n![gen_todo](https://user-images.githubusercontent.com/73610201/211216011-27e057b0-0420-4d90-8950-999f75583566.gif)\n\nThis command will print out all TODO comments that were found in the code, sorted by their prioritization: urgent, soon and regular. \n_Urgent_ tasks will be printed in RED, _soon_ in CYAN and _regular_ comments in WHITE to make it easier to read. There is also an option to filter comments by their priotization:\n```\n# Prints urgent TODOs\ntodo -u [folder/file]\n```\n![urgent_todo](https://user-images.githubusercontent.com/73610201/211216002-c00860d3-7a61-425f-8cb2-939de85c01ec.gif)\n\nOr:\n```\n# Prints soon TODOs\ntodo -s [folder/file]\n```\n![soon_todo](https://user-images.githubusercontent.com/73610201/211216007-f4eabb81-76d0-42c5-9334-0f13857e809b.gif)\n\nComments can also be assigned to a user by adding "Todo @username" comment:\n```\n# Prints soon TODOs\ntodo -a [USERNAME] [folder/file]\n```\n\n![assigned_todo](https://user-images.githubusercontent.com/73610201/211216263-ca453589-e490-49b3-a839-65315366f34f.gif)\n\nFinally, there is an option to save the list in a text file (stores as regular text without colors):\n```\n# Store results in a txt file![dummy](https://user-images.githubusercontent.com/73610201/211216021-a4859641-69a6-4e94-8f8c-2c0cafd0a455.png)\n\ntodo -o [path/to/sample.txt] [folder/file]\n```\n\n## Setup\n```\npip install todocom\n```\n\n## Comments Format\nThere are two types of comments: single line and multi-line. Currently, multi-line comments (docstrings) are only supported in Python, but single line should work for most programming languages.\n\nFormat is flexible and can be lower-case, upper-case or a combination of both. Below are several examples:\n```\n1. TODO:\n2. TODo:\n3. TOD0:\n4. ToD0:\n5. To-D0:\n6. to-do:\n```\n\nIn _Urgent_ and _soon_ comments the TODO part is flexible as shown above, but must be followed by either _urgent_ or _soon_ in lower-case:\n ```\n1. TO-DO soon:\n2. tODo soon: \n3. ToD0 urgent:\n4. T0-D0 urgent:\n```\n',
    'author': 'avivfaraj',
    'author_email': 'avivfaraj4@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/avivfaraj/todocom',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
