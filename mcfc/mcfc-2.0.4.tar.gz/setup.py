from setuptools import setup
import io

with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()


setup(name="mcfc",
    author="woidzero",
    version="2.0.4",
    license="MIT",
    url="https://github.com/woidzero/MCFC",
    description="Text formatting using Minecraft color codes.", 
    packages=["mcfc"], 
    author_email="woidzeroo@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
)