
from distutils.core import setup

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="scpQCA",
    version="0.1.5",
    author="Manqing FU",
    author_email="fumanqing@outlook.com",
    description="a new and more powerful QCA algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['matplotlib','sklearn'], # 比如["flask>=0.10"]
    license='Apache 2.0',
    url="https://github.com/Kim-Q/scpQCA",
    packages=setuptools.find_packages(),
    platforms=["all"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)