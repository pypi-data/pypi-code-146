"""
"""
from os.path import abspath, dirname, join

# To use a consistent encoding
from codecs import open

# Always prefer setuptools over distutils
from setuptools import setup

# This call to setup() does all the work
setup(
    name="imagem_etl",
    version="0.1.1",
    description="ETL da Imagem (Utilities)",
    long_description=open(join(abspath(dirname(__file__)), "README.md"), encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    # url="<<azure-git-repo>>",
    # author="Felipe Fernandes",
    # author_email="ffernandes@img.com.br",
    # license="MIT",
    # classifiers=[
    #     "Intended Audience :: Developers",
    #     "License :: OSI Approved :: MIT License",
    #     "Programming Language :: Python",
    #     "Programming Language :: Python :: 3",
    #     "Programming Language :: Python :: 3.6",
    #     "Programming Language :: Python :: 3.7",
    #     "Programming Language :: Python :: 3.8",
    #     "Programming Language :: Python :: 3.9",
    #     "Operating System :: OS Independent"
    # ],
    packages=["imagem_etl"],
    include_package_data=True,
    install_requires=["pyodbc", "pandas"]
)
