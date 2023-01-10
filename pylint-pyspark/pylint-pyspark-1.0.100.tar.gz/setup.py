from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pylint-pyspark",
    version="1.0.100",
    author="Aman Ankit",
    author_email="aman@astrumu.com",
    description="PySpark Style Guide",
    long_description="Built on Palantir's PySpark Style Guide, this is a guide to PySpark code style presenting common situations and the associated best practices based on the most frequent recurring topics across the PySpark repos we've encountered.",
    long_description_content_type="text/markdown",
    url="https://github.com/AstrumU/pylint-pyspark",
    packages=["pylint_pyspark"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pylint"],
)
