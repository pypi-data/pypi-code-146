#!/usr/bin/python3
from setuptools import find_packages, setup


def get_file_content_as_list(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as file:
        content = [line.strip() for line in file]
    return content


def get_file_content(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


packages = find_packages()
print(f"Found packages: {packages}")
VERSION = get_file_content("VERSION")
INSTALL_REQUIRES = get_file_content_as_list("requirements.txt")
DOCUMENTATION_MD = get_file_content("README.md")

setup(
    name="auto-group",
    version=VERSION,
    author="Ales Adamek, Filip Cima",
    author_email="alda78@seznam.cz",
    description="Tools for creating tree structures from flat list of dicts",
    long_description=DOCUMENTATION_MD,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/alda78/auto-group",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
    include_package_data=False,  # MANIFEST.in
    zip_safe=False,  # aby se spravne vycitala statika pridana pomoci MANIFEST.in
)
