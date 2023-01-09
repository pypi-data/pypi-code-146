from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'dikas project'
LONG_DESCRIPTION = 'dikas project long description'

# Setting up
setup(
    name="dikaspackforeva",
    version=VERSION,
    author="dika foreva",
    author_email="<goga.samunashvili@yahoo.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['psutil'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    entry_points={
        'console_scripts': [
            'snapshot = dikaspackage.hello:main'
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
