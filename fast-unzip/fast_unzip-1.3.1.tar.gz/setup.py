# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_unzip']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['fast_unzip = fast_unzip.fast_unzip:main']}

setup_kwargs = {
    'name': 'fast-unzip',
    'version': '1.3.1',
    'description': 'Fast multithread/multiprocess unzipper',
    'long_description': '# Fast unzipper\n\nFast unzipper is a Python CLI tool you could use to effectively and fast unzip ZIP archives.\n\n## When will it be helpful?\n\nIt proved to be useful working with huge amount of relatively small files for it distributes load among processes and threads to provide higher speeds than standard unzip.\n\nHowever, should you need to unzip archive with only few files, that tool isn\'t probably for you because it won\'t be possible to distribute 1 or 2 files in archive among threads.\n\nMoreover, changing threads(e.g. 8) when there are 8 files will lead to decrease in performance rather than profit in time.\n\nUse it when it\'s possible to adequately split your files.\n\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install fast_unzip.\n\n```bash\npip install fast_unzip\n```\n\n## Usage\nIt\'s compulsory you specify the archive PATH like this.\n\nMacOS/Linux\n```bash\npython3 -m fast_unzip test.zip\n```\nWindows\n```bash\npython -m fast_unzip test.zip\n```\nBeing started this way it will use standard mode which means it will decide automatically which mode to use depending on compression level of your archive.\n\nStandard directory for unpacking is ./ZIP_unpack.\nYou can specify it with -d flag.\n```bash\npython -m fast_unzip test.zip -d ./../test\n```\n\nNevertheless, you can specify number of processes and threads you want to start using -p and -t flags.\n```bash\npython3 -m fast_unzip test.zip -p 4 -t 10\n```\nAlso, you can specify mode you want this tool to work. Maybe you know beforehand that compression level is low. You do it with -m flag.\n```bash\npython -m fast_unzip test.zip -m "mt"\n```\n## Recommendations\nThough, it\'s possible to choose mode, number of threads and number of processes manually, it\'s highly unrecommended, because if will affect the performance.\n\nNumber of threads is chosen as `min(32, os.cpu_count())`.\n\nNumber of processes is chosen as `os.cpu_count()`.\n\nFor some reasons `os.cpu_count()` can fail to determine your system characteristics. This way you\'ll be given an error and you need to specify this arguments explicitly. I highly recommend you use formula from above.\n\nIf you try to enter more processes than `os.cpu_count()`\nfound you\'ll be given an error. You can either choose an appropriate number of processes or leave it to program to decide.\n\n**!!! If it\'s impossible for `os.cpu_count()` to work and you enter inappropriate number of processes it will lead to undefined behaviour.**\n\nIf you know that archive you want to unpack is compressed less than 50% you can use `-m "cmbd"`, else `-m "mt"`. It will disable part of program doing analysis and increase performance.\n\nThank you for using our tool!\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Nikita Pshenko',
    'author_email': 'pshenko1999@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Inferno2899/fast_unzip.git',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
