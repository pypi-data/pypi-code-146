# following https://www.youtube.com/watch?v=tEFkHEKypLI&t=176s und https://www.youtube.com/watch?v=GIF3LaRqgXo 12:48 / 29:26

# cd -> current dir
# cd "C:\Users\Creed\OneDrive\Schul-Dokumente\Programmieren\Python\Code Sammlung\Packages\creating_colorful_terminal"

# python setup.py sdist bdist_wheel

# install current package but not in site-packages -> link to this
# pip install -e .


# twine upload dist/*
# twine upload --skip-existing dist/*
# twine upload --verbose --skip-existing dist/*
# twine upload --verbose dist/*

from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.3"
DESCRIPTION = (
    "Print with color, style your output and take full control of your terminal."
)

# Setting up
setup(
    name="colorful_terminal",
    version=VERSION,
    author="André Herber",
    author_email="andre.herber.programming@gmail.com",
    url="https://github.com/ICreedenI/colorful_terminal",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=[
        "python",
        "print",
        "color",
        "colour",
        "colored",
        "coloured",
        "rainbow",
        "terminal",
        "console",
        "colorama",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Terminals",
    ],
)
