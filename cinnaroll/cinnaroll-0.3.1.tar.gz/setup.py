#!/usr/bin/env python3

from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), mode="r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cinnaroll",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Configuring, Packaging and Sending Machine Learning Models to Deployment at cinnaroll.ai",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="VirtusLab",
    author_email="service@cinnaroll.ai",
    url="https://github.com/carthago-cloud/cinnaroll-python-lib",
    license="Apache License 2.0",
    keywords="machine-learning,ml,deployment",
    packages=["cinnaroll", "cli", "cinnaroll_internal"],
    entry_points={
        "console_scripts": [
            "cinnaroll-login=cli.login:main",
        ]
    },
    python_requires=">=3.7, <4",
    install_requires=[
        "toml>=0.10.2",
        "requests>=2.28.1",
        "Pillow>=9.2.0",
        "traitlets>=5.5.0",
        "asttokens>=2.1.0",
    ],
    classifiers=[
        # See https://pypi.org/classifiers/
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    options={"bdist_wheel": {"universal": "1"}},
    include_package_data=True,
)
