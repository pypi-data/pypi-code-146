# This file is part of fastapi_tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import io
import os
import re
from setuptools import setup


def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()


def get_version():
    init = read('version.py')
    return re.search("__version__ = '([0-9.]*)'", init).group(1)


setup(name='fastapi_tryton',
    version=get_version(),
    author='PRESIK SAS',
    author_email='gerente@presik.com',
    url='https://bitbucket.org/presik/fastapi-tryton',
    description='Adds Tryton support to FastAPI application',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    py_modules=['fastapi_tryton', 'version'],
    zip_safe=False,
    platforms='any',
    keywords='fastapi tryton web',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Tryton',
        'Framework :: FastAPI',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    license='GPL-3',
    python_requires='>=3.7',
    install_requires=[
        'uvicorn',
        'fastapi>=0.85',
        'trytond>=6.0',
        'wheel',
    ])
