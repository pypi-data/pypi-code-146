"""
Python3 stub library for Alphalogic adapters.
"""

import sys
import distro
from setuptools import setup
from alphalogic_api3 import __version__

cur = 'win32' if sys.platform == 'win32' else distro.like().lower()
ext = '.zip' if sys.platform == 'win32' else '.tar.gz'

bin_name = 'alphalogic_api3-%s-%s%s' % (cur, __version__, ext)

if __name__ == '__main__':
    with open('README.md', 'r') as fh:
        long_description = fh.read()

    setup(
        name='alphalogic_api3',
        version=__version__,
        description=__doc__.replace('\n', '').strip(),
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Alphaopen',
        author_email='mo@alphaopen.com',
        url='https://github.com/Alphaopen/alphalogic_api3',
        py_modules=['alphalogic_api3'],
        include_package_data=True,
        setup_requires=['wheel'],
        packages=[
            'alphalogic_api3',
            'alphalogic_api3.objects',
            'alphalogic_api3.protocol',
            'alphalogic_api3.tests'
        ],
        classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        license='MIT',
        platforms=['linux2', 'win32'],
        python_requires='>=3.8',
        install_requires=[
            'grpcio~=1.51.1',
            'grpcio-tools~=1.51.1',
            'distro',
        ],
    )
