from setuptools import setup, find_packages

VERSION = "1.0.7"

with open("README.md", encoding="utf8", mode="r") as f:
    LONG_DESCRIPTION = f.read()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="python_simple_menu",
    version=VERSION,
    author="Chris Vann",
    author_email="chrisvann01@gmail.com",
    description="A simple console menu",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/ripvannwinkler/python-simple-menu",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.7",
    keywords=["python", "menu", "simple menu", "console menu"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
    ],
)
