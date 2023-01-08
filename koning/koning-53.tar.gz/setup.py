#!/usr/bin/env python3
# This file is placed in the Public Domain.


import os


from setuptools import setup, find_packages


def read():
    return open("README.rst", "r").read()


def uploadlist(dir):
    upl = []

    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)
    return upl

setup(
    name='koning',
    version='53',
    url='https://bitbucket.org/bthate/koning',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="@KarimKhanQC reconsider OTP-CR-117/19",
    license='Public Domain',
    zip_safe=True,
    packages=["koning"],
    long_description=read(),
    include_package_data=True,
    data_files=[("share/doc/koning", uploadlist("docs"))],
    scripts=["bin/koning"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: Public Domain',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
