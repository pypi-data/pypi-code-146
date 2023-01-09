from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="pyanalysis",
    version="2.0.8.5",
    license="MIT",
    description="Python Library for pyanalysis.ptsecurity.tech",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author="Stanislav Rakovsky",
    author_email="iam@disasm.me",
    install_requires=required,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
