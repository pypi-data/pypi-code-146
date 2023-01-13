from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "pandas",
    'filelock==3.9.0',
]

setup(
    name="csv.py",
    version="0.5.1",
    author="Tao Xiang",
    author_email="tao.xiang@tum.de",
    description="A package of tools for csv files",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/leoxiang66/csv-toolkit",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
  "Programming Language :: Python :: 3.8",
  "License :: OSI Approved :: MIT License",
    ],
)