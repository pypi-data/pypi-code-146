import os
import re
from setuptools import setup

_long_description = """
### How to import the Rubik's library

``` bash
from rubiJeff import jeff
```

### How to install the library

``` bash
pip install rubiJeff
```
"""

setup(
    name = "rubiJeff",
    version = "1.1.2",
    author = "rubiJeff",
    author_email = "an8060703@gmail.com",
    description = ("Robot Rubika rubiJeff"),
    license = "MIT",
    keywords = ["rubika","bot","robot","library","Rubika","Python","rubiJeff","RubiJeff"],
    url = None,
    packages=['rubiJeff'],
    long_description=_long_description,
    long_description_content_type = 'text/markdown',
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: Implementation :: PyPy",
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11'
    ],
)
