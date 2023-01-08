"""Setup configuration for the package."""
# -*- coding: utf-8 -*-
try:
    from setuptools import find_packages, setup
    import versioneer
except ImportError:
    import distribute_setup

    distribute_setup.use_setuptools()
    from setuptools import setup, find_packages
    import versioneer

# pylint: disable=invalid-name
long_desc = """cloud object storage wrapper"""

requires = ["esdk-obs-python"]

setup(
    name="wareroom",
    url="https://github.com/lipicoder/wareroom",
    author="lipi",
    author_email="lipicoder@qq.com",
    version = versioneer.get_version(),
    cmdclass = versioneer.get_cmdclass(),
    description= long_desc,
    long_description=long_desc,
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
)
