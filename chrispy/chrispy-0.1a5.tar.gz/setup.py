import os

import setuptools


def long_description():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        return f.read()


def requirements():
    with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), encoding='utf-8') as f:
        return f.read().splitlines()


setuptools.setup(
    name="chrispy",
    version="0.1a5",
    license='MIT',
    author='Jihee Ryu',
    author_email='chrisjihee@naver.com',
    description="common functions for Python 3",
    long_description=long_description(),
    url="https://github.com/chrisjihee/chrispy",
    packages=setuptools.find_packages(),
    package_data={},
    include_package_data=True,
    install_requires=requirements(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
