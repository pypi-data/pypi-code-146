#!/usr/bin/env python3
# This file is placed in the Public Domain.


import os


from setuptools import setup


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
    name='kamer',
    version='41',
    url='https://github.com/bthate/kamer',
    author='Bart Thate',
    author_email='bthate67@gmail.com',
    description="@KarimKhanQC reconsider OTP-CR-117/19",
    license='Public Domain',
    zip_safe=True,
    scripts=["bin/kamer"],
    packages=["kamer"],
    long_description=read(),
    include_package_data=True,
    data_files=[("share/doc/kamer", uploadlist("docs"))],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: Public Domain',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
