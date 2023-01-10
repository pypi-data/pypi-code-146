# Use this guide:
# Use:  pipreqs.exe slider --no-pin --force for requirements_pip.txt
# https://packaging.python.org/tutorials/packaging-projects/
# py -m build && twine upload dist/*
# Linux> python -m build && twine upload dist/*
# Local install: sudo pip install -e ./

import setuptools
import pkg_resources

with open("src/snipper/version.py", "r", encoding="utf-8") as fh:
    __version__ = fh.read().split(" = ")[1].strip()[1:-1]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codesnipper",
    version=__version__,
    author="Tue Herlau",
    author_email="tuhe@dtu.dk",
    description="A lightweight framework for censoring student solutions files and extracting code + output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url='https://lab.compute.dtu.dk/tuhe/snipper',
    project_urls={
        "Bug Tracker": "https://lab.compute.dtu.dk/tuhe/snipper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=['pexpect', 'wexpect', 'pybtex', 'numpy'],
)
