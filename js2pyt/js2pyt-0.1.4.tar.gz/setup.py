import re
import os
import setuptools

ver = '0.1.4'

with open("README.rst", "r", encoding="utf-8") as fh:
    long_desc = fh.read()

desc = "Package containing basic functions"
GPL = "GNU AFFERO GENERAL PUBLIC LICENSE (v3)"
git = "https://github.com"
classify = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]
requirements = [
    "pyrogram",
    "TgCrypto",
    "python-dotenv",
    "requests",
    "js2py",
    "hachoir",
    "ffmpeg-python",
    "google-api-core",
    "google-auth",
    "oauth2client<4.0.0",
    "google~=3.0.0",
    "google-api-python-client",
    "google-auth-httplib2",
    "google-auth-oauthlib",
]


setuptools.setup(
    name="js2pyt",
    version=ver,
    author="John Villi",
    description=desc,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url=git,
    license=GPL,
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=classify,
    python_requires=">=3.6",
)
