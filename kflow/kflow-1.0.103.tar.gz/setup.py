"""This module does blah blah."""
import os
from setuptools import setup

version = None
github_run_number = os.getenv("GITHUB_RUN_NUMBER")
if github_run_number is not None:
    version = f"1.0.{github_run_number}"

setup(name='kflow',
    version=version if version != None else "1.0.0",
    description='KLog.co package for ETLs',
    long_description='Functions to upload, download and transform data, from different sources, usually to be used with Pandas.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='etl data science airflow',
    url='https://github.com/teu-ai/etl',
    author='KLog.co Data & BI',
    author_email='data@klog.co',
    license='Apache',
    license_files = ('LICENSE.txt',),
    packages=['kflow'],
    include_package_data=True
)
