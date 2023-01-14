from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'My Library'
LONG_DESCRIPTION = 'A Library contains mathmodule and hellomodule'

# Setting up
setup(
    name="mylibraryPHDDSM007",
    version=VERSION,
    author="QAMAR_PHDDSM007",
    author_email="qamaruzaman9999@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'pythonlibrary', 'mylibrary', 'mathmodule', 'helloword'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)