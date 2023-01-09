from setuptools import setup


setup(
    name="supply-chain-demo",
    description="Supply Chain Demo",
    long_description="Supply Chain Demo",
    long_description_content_type="text/markdown",
    author="Demo",
    license="Apache License, Version 2.0",
    version="0.1.1",
    packages=["demo"],
    install_requires=["requests"],
    python_requires=">=3.7",
)