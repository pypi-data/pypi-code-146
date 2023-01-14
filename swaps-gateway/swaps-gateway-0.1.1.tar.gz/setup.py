from setuptools import setup, find_packages

with open("README.md") as readme:
    long_description = readme.read()

setup(name='swaps-gateway', packages=find_packages("src"))
