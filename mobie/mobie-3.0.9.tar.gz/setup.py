from setuptools import setup
from distutils.command.build_py import build_py

import os

install_requires=[
    'jgo>=0.4.0',
]

entry_points={
    'console_scripts': [
        'mobie=mobie:launch_mobie',
#        'generate-mobie-bash-completion=mobie:generate_mobie_bash_completion'
    ]
}

name = 'mobie'

setup(
    name=name,
    version="3.0.9",
    author='Christian Tischer',
    author_email='christian.tischer@embl.de',
    maintainer="Christian Tischer",
    maintainer_email="christian.tischer@embl.de",
    description='mobie',
    url='https://github.com/mobie/mobie-viewer-fiji',
    packages=['mobie'],
    entry_points=entry_points,
    install_requires=install_requires)
