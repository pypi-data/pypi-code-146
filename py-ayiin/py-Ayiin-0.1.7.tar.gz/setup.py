import re

import setuptools


with open("requirements.txt", encoding="utf-8") as r:
    requirements = [i.strip() for i in r]

with open("pyAyiin/__init__.py", "rt", encoding="utf8") as x:
    version = re.search(r'__version__ = "(.*?)"', x.read()).group(1)

with open("pyAyiin/__init__.py", "rt", encoding="utf8") as x:
    license = re.search(r'__license__ = "(.*?)"', x.read()).group(1)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


name = "py-Ayiin"
author = "AyiinXd"
author_email = "ayingaming98@gmail.com"
description = "A Secure and Powerful Python-Telethon Based and Python-Pyrogram Based Library For Your Userbot Module."
url = "https://github.com/AyiinXd/AyiinXd"
project_urls = {
    "Bug Tracker": "https://github.com/AyiinXd/AyiinXd/issues",
    "Source Code": "https://github.com/AyiinXd/AyiinXd",
}
classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]

setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    project_urls=project_urls,
    license=license,
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=classifiers,
    python_requires="~=3.7",
)
