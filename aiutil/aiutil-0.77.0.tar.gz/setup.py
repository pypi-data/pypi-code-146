# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiutil', 'aiutil.hadoop', 'aiutil.notebook']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.0.0',
 'PyYAML>=5.3.1',
 'dateparser>=0.7.1',
 'dulwich>=0.20.24',
 'loguru>=0.3.2',
 'notifiers>=1.2.1',
 'numba>=0.53.0rc1.post1',
 'pandas-profiling>=2.9.0',
 'pandas>=1.2.0',
 'pathspec>=0.8.1',
 'pytest>=3.0',
 'python-magic>=0.4.0',
 'scikit-image>=0.18.3',
 'sqlparse>=0.4.1',
 'toml>=0.10.0',
 'tqdm>=4.59.0']

extras_require = \
{':extra == "jupyter" or extra == "all"': ['black>=22.12.0,<23.0.0'],
 'admin': ['psutil>=5.7.3'],
 'all': ['psutil>=5.7.3',
         'opencv-python>=4.0.0.0',
         'pillow>=7.0.0',
         'networkx>=2.5',
         'docker>=4.4.0',
         'requests>=2.20.0',
         'PyPDF2>=1.26.0',
         'nbformat>=5.0.7',
         'nbconvert>=5.6.1'],
 'cv': ['opencv-python>=4.0.0.0', 'pillow>=7.0.0'],
 'docker': ['networkx>=2.5', 'docker>=4.4.0', 'requests>=2.20.0'],
 'jupyter': ['nbformat>=5.0.7', 'nbconvert>=5.6.1'],
 'pdf': ['PyPDF2>=1.26.0']}

entry_points = \
{'console_scripts': ['logf = aiutil.hadoop:logf.main',
                     'match_memory = aiutil:memory.main',
                     'pykinit = aiutil.hadoop:kerberos.main',
                     'pyspark_submit = aiutil.hadoop:pyspark_submit.main',
                     'repart_hdfs = aiutil.hadoop:repart_hdfs.main',
                     'snb = aiutil.notebook:search.main']}

setup_kwargs = {
    'name': 'aiutil',
    'version': '0.77.0',
    'description': 'A utils Python package for data scientists.',
    'long_description': "# [aiutil](https://github.com/legendu-net/aiutil): Data Science Utils\n\nThis is a Python pacakage that contains misc utils for Data Science.\n\n1. Misc enhancement of Python's built-in functionalities.\n    - string\n    - collections\n    - pandas DataFrame\n    - datetime\n2. Misc other tools\n    - `aiutil.git`: check and report modified but unpushed repository under a directory recursively\n    - `aiutil.filesystem`: misc tools for querying and manipulating filesystems; convenient tools for manipulating text files.\n    - `aiutil.url`: URL formatting for HTML, Excel, etc.\n    - `aiutil.sql`: SQL formatting\n    - `aiutil.cv`: some more tools (in addition to OpenCV) for image processing\n    - `aiutil.shell`: parse command-line output to a pandas DataFrame\n    - `aiutil.shebang`: auto correct SheBang of scripts\n    - `aiutil.poetry`: tools for making it even easier to manage Python project using Poetry\n    - `aiutil.pdf`: easy and flexible extracting of PDF pages\n    - `aiutil.memory`: query and consume memory to a specified range\n    - `aiutil.jupyter`: Jupyter/Lab notebook related tools (cell code formating, converting, etc.)\n    - `aiutil.dockerhub`: managing Docker images on DockerHub in batch mode using Python\n    - `aiutil.hadoop`: \n        - A Spark application log analyzing tool for identify root causes of failed Spark applications.\n        - Pythonic wrappers to the `hdfs` command.\n        - A auto authentication tool for Kerberos.\n        - An improved version of `spark_submit`.\n        - Other misc PySpark functions. \n    \n## Supported Operating Systems and Python Versions\n\n| OS      | Python 3.7 | Python 3.8 | Python 3.9 | Python 3.10 |\n|---------|------------|------------|------------|-------------|\n| Linux   | Y          | Y          | Y          | Y           |\n| macOS   | Y          | Y          | Y          | Y           |\n| Windows | Y          | Y          | Y          | Y           |\n\n## Installation\n\n```bash\npip3 install --user -U aiutil\n```\nUse the following commands if you want to install all components of aiutil. \nAvailable additional components are `cv`, `docker`, `pdf`, `jupyter`, `admin` and `all`.\n```bash\npip3 install --user -U aiutil[all]\n```\n",
    'author': 'Benjamin Du',
    'author_email': 'longendu@yahoo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/legendu-net/aiutil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
