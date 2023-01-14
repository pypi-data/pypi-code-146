import os.path
import codecs

from setuptools import find_packages, setup

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='netbox-users-and-computers',
    version=get_version('users_and_computers/version.py'),
    description='Netbox plugin. Manage AD Users and Workstations',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    download_url='https://pypi.org/project/netbox-users-and-computers/',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords=['netbox', 'netbox-plugin'],
    author='Artur Shamsiev',
    author_email='me@z-lab.me',
    maintainer='Artur Shamsiev',
    maintainer_email='me@z-lab.me',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

