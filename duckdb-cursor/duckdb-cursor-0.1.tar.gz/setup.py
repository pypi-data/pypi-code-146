from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="duckdb-cursor",
    version="0.1",
    author="Wagner Corrales",
    author_email="wagnerc4@gmail.com",
    description="DuckDB cursor wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/wcorrales/duckdb-cursor",
    packages=["duckdb_cursor"],
    install_requires=["duckdb"],
    license="GNU",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
)
