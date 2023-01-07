# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast
import re
from setuptools import setup, find_packages
from os import path


_version_re = re.compile(r"__version__\s+=\s+(.*)")


with open("canner/__init__.py", "rb") as f:
    version = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "public_readme.md"), encoding="utf-8") as f:
    long_description = f.read()

tests_require = [
    "pytest>=6.2.2",
    "pytest-runner>=5.3.1; python_version >='3.7' and python_version <'3.9'",
    "pytest-runner==5.3.1; python_version >='3.6' and python_version <'3.7'"
]


setup(
    name="canner-python-client",
    author="Canner Team",
    author_email="contact@canner.io",
    version=version,
    url="https://github.com/canner/canner-python-client",
    packages=find_packages(),
    package_data={"": ["LICENSE", "README.md"]},
    description="Client for the Canner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    dependency_links=[
        'https://pypi.python.org/simple'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Database :: Front-Ends",
    ],
   
    install_requires=[
        "pillow>=8.1.2",
        "pyarrow>=3.0.0",
        "json-lines>=0.5.0",
        "requests>=2.25.1",
        "aiohttp>=3.7.4",
        "nest-asyncio>=1.5.1",
        "bleach==4.1.0",
        "dataclasses>=0.8; python_version >='3.6' and python_version <'3.7'",
        "pandas>=1.1.5, <=1.2; python_version >='3.7' and python_version <'3.9'",
        "pandas==0.25.3; python_version >='3.6' and python_version <'3.7'",
        # numpy should >= 1.19.5 to let python install newer version depends on different python version) for supporting python3.7.x - python 3.8.x environment work 
        # solve numpy.ndarray size changed, may indicate binary incompatibility. Expected 88 from C header, got 80 from PyObject issue
        "numpy>=1.22.0, <1.23; python_version >='3.8' and python_version <'3.9'",
        "numpy>=1.20.0, <1.21; python_version >='3.7' and python_version <'3.8'",
        "numpy==1.19.5; python_version >='3.6' and python_version <'3.7'",
        "fastparquet==0.4.1",
        "numba==0.53.1; python_version >='3.8' and python_version <'3.9'",
        
    ],
    tests_require=tests_require,
    python_requires='>=3.6.0, <3.9'
)
