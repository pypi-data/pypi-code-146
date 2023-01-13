# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
Set scaling factor of images and figures depending on the builder.
'''

requires = ['Sphinx>=1.6']

setup(
    name='sphinxcontrib-scalebybuilder',
    version='0.1.1',
    url='https://github.com/missinglinkelectronics/sphinxcontrib-scalebybuilder',
    download_url='https://pypi.org/project/sphinxcontrib-scalebybuilder',
    license='BSD',
    author='Stefan Wiehler',
    author_email='sphinx_contribute@missinglinkelectronics.com',
    description='Sphinx scale image by builder extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    python_requires='~=3.4',
    namespace_packages=['sphinxcontrib'],
)
