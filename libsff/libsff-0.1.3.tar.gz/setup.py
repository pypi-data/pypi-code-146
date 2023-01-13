from setuptools import setup


with open("requirements.txt", "r") as file:
    requirements = file.read().splitlines()

version = "0.1.3"

with open("README.md", "r") as file:
    readme = file.read()

setup(
    name="libsff",
    author="NandeMD",
    url="https://github.com/NandeMD/libsff",
    version=version,
    license="GPL-3.0",
    description='A Pyhon parser for sff files.',
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=["wheel"] + requirements,
    python_requires=">=3.8.0",
    packages=["libsff"],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries'
    ]
)