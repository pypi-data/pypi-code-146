

import os
from setuptools import setup, find_packages
# REQUIRES = [
#     "certifi>=2020.04.01",
#     "python-dateutil>=0.1.0",
#     "urllib3>=1.0"
# ]

PACKAGE = "PaasSdk"
NAME = "RongyingPaasSdk" or "rongyingPaas-package"
DESCRIPTION = "rongyingyun  Paas SDK Library for Python"
AUTHOR = "rongyingyun Paas SDK"
AUTHOR_EMAIL = "xdy@cyjcloud.com"
URL = "https://gitee.com/ccgkxdy/paas-sdk-python"
VERSION = __import__(PACKAGE).__version__

LONG_DESCRIPTION = ''
if os.path.exists('./README.md'):
    with open("README.md", encoding='utf-8') as fp:
        LONG_DESCRIPTION = fp.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Apache License 2.0",
    url=URL,
    keywords=["rongyingyun", "RongyingPaasSdk"],
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    platforms="any",
    # install_requires=REQUIRES,
    python_requires=">=3",
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Topic :: Software Development"
    ), install_requires=['requests']
)
