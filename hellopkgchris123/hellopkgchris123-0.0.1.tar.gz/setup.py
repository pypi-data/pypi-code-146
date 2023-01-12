from setuptools import setup, find_packages
import codecs
import os

# python3 setup.py sdist bdist_wheel
VERSION = "0.0.1"
DESCRIPTION = "basic hello package"

# Setting up
setup(
    name="hellopkgchris123",
    version=VERSION,
    author="ChrisLee (Chris Gi Hong Lee)",
    author_email="<gihonglee20@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "video", "stream", "video stream", "camera stream", "sockets"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
