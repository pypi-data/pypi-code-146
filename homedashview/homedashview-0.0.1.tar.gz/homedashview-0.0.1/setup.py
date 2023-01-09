from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'First project to create a dashboard of available smarthome devices'
LONG_DESCRIPTION = 'First project to create a dashboard of available smarthome devices'

# Setting up
setup(
    name="homedashview",
    version=VERSION,
    author="RoBiApps007 (Robert Binder)",
    author_email="<robert.rothschaedl@hotmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)