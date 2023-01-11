"""
Setup the Python package
"""

import pathlib
import re
from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

WORK_DIR = pathlib.Path(__file__).parent


def get_version():
    """ Get version """

    txt = (WORK_DIR / 'consys' / '__init__.py').read_text('utf-8')

    try:
        return re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    except IndexError as e:
        raise RuntimeError('Unable to determine version') from e


setup(
    name='consys',
    version=get_version(),
    description='Base object model for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kosyachniy/consys',
    author='Alexey Poloz',
    author_email='alexypoloz@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    keywords=(
        'base, object, model, oop, orm, python, mongodb, files, uploading, '
        'handlers, errors, types, checking'
    ),
    packages=find_packages(exclude=('tests',)),
    python_requires='>=3.7, <4',
    install_requires=[
        'pymongo==4.3.3',
        'Pillow==9.4.0',
        'requests',  # Because of conflicts with main repo
        'pydantic==1.10.4',
    ],
    project_urls={
        'Source': 'https://github.com/kosyachniy/consys',
    },
    license='MIT',
    include_package_data=False,
)
