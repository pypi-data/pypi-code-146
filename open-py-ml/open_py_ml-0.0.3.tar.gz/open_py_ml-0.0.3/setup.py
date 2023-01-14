from setuptools import setup, find_packages

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name="open_py_ml",
    version="0.0.3",
    author="Adam Elsayed Gewely",
    author_email="adam.gewely@gmail.com",
    description="A simple, Open source ML library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adammgewely/open-py-ml",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "difflib",
        "json"
    ],
)
