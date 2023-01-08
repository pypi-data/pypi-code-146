from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open("requirements.txt", "r") as req_file:
    requirements = req_file.read().split("\n")

setup(
    name="podlozhnyy_module",
    version="1.2",
    description="One place for the most useful methods for work",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Nikita Podlozhnyy",
    author_email="podlozhnyy.ne@phystech.edu",
    python_requires=">=3.7.0",
    url="https://github.com/NPodlozhniy/podlozhnyy-module",
    license="MIT",
    # find packages only, doesn't install files tht doesn't belong to any package
    packages=find_packages(),
    # have to provide module name in the separate argument 
    py_modules=["podlozhnyy_module"],
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
)