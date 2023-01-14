import codecs
import os.path

from setuptools import find_packages, setup


with open("README.md", "r") as fh:
    long_description = fh.read()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='netbox-users-and-computers',
    version=get_version('users_and_computers/version.py'),
    description='Netbox plugin. Manage AD Users and Workstations',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://pypi.org/project/netbox-users-and-computers/',
    author='Artur Shamsiev',
    author_email='me@z-lab.me',
    keywords=['netbox', 'netbox-plugin'],
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
