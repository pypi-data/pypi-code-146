import os
from setuptools import setup, find_packages


this_dir = os.path.dirname(__file__)

with open(os.path.join(this_dir, "README.md"), "rb") as fo:
    long_description = fo.read().decode("utf8")

with open(os.path.join(this_dir, 'requirements.txt')) as fo:
    requirements = fo.read().splitlines()

dev_requirements = [
    "flake8~=3.9.2",
    'pytest~=6.2.4',
    'pytest-mock~=3.6.1',
    'pytest-cov~=2.12.1',
    'fastparquet~=0.8.0'
]

setup(
    # Application name:
    name="COMPREDICT-AI-SDK",

    # Version number:
    use_scm_version=True,
    setup_requires=['setuptools_scm'],

    # Application author details:
    author="Ousama Esbel",
    author_email="esbel@compredict.de",

    # Packages
    packages=find_packages(),

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/compredict/ai-sdk-python",

    license="MIT",
    description="Connect Python applications with COMPREDICT AI Core.",
    keywords=["COMPREDICT", "AI", "SDK", "API", "rest"],
    long_description_content_type="text/markdown",
    long_description=long_description,

    # Dependent packages (distributions)
    install_requires=requirements,
    extras_require={
            'dev': dev_requirements
    }
)
