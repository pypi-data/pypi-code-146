import os
from setuptools import setup, find_packages, find_namespace_packages


def find_version(*args):
    """ Find version string starting with __version__ in a file"""

    f_path = os.path.join(os.path.dirname(__file__), *args)
    with open(f_path) as f:
        for line in f:
            if line.startswith('__version__'):
                break
    version_strings = line.split('"')
    if len(version_strings) != 3:
        raise ValueError('Version string is not enclosed inside " ".')
    return version_strings[1]


description = open('README.md').read()
version_string = find_version('srsinst/sr860', '__init__.py')

setup(
    name='srsinst.sr860',
    version=version_string,
    description='Communication package for SRS Lock-In Amplifier SR860 series',
    packages=['srsinst.sr860', 'srsinst.sr860.instruments', 'srsinst.sr860.instruments.sr865',
              'srsinst.sr860.tasks', 'srsinst.sr860.plots'],
             # find_namespace_packages(),
    package_data={
        'srsinst.sr860': ['*.taskconfig']
    },
    # include_package_data=True,
    long_description=description,
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    install_requires=[
        "numpy",
        "python-vxi11",
        "srsgui>=0.1.7"
    ],
    extras_require={
        'gui': ['matplotlib', 'pyside2']
    },
    entry_points={
        'console_scripts': [
            'sr860 = srsinst.sr860.__main__:main'
        ],
    },

    license="MIT license",
    keywords=["SR860", "SR865A", "SRS", "Stanford Research Systems"],
    author="Chulhoon Kim",
    # author_email="chulhoonk@yahoo.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics"
    ]
)
