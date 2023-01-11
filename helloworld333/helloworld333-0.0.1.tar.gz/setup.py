from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name='helloworld333',
    version='0.0.1',
    description='Say hello',
    py_modules=["helloworld"],
    package_dir={'':'src'},
    classifiers =[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)