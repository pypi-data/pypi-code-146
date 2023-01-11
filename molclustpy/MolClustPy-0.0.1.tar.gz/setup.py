import setuptools
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A Python package to analyze multivalent biomolecular clustering.'


# Setting up
setuptools.setup(
    name="MolClustPy",
    version=VERSION,
    author="",
    author_email="",
    description=DESCRIPTION,
    packages=setuptools.find_packages(),
    install_requires=['bionetgen', 'numpy', 'matplotlib', 'pandas'],
    keywords=['', '', '', '', '', ''],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)