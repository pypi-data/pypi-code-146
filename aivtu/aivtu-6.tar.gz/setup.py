from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
VERSION = '6'
DESCRIPTION = 'AI/ML programs'
LONG_DESCRIPTION = 'VTU lab programs.'

# Setting up
setup(
    name="aivtu",
    version=VERSION,
    author="Sanjay R",
    author_email="<sanjay66r@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['vtu'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
