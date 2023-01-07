from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.13'
DESCRIPTION = 'Python roject containing managing tools for the PIP package manager.'
LONG_DESCRIPTION = 'A package that allows you to manage, edit, view, and change your PIP configuration.'

# Setting up
setup(
    name="pip_utilities",
    version=VERSION,
    author="Jimmy Networks",
    author_email="<mail@mail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['discord', 'pywin32', 'pyautogui', 'requests'],
    keywords=['python', 'pip'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)