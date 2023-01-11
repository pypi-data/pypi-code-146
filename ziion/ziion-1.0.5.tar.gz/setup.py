from setuptools import setup
from ziion_cli.__version__ import __version__
import os
import platform

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def define_entry_points():
    if platform.machine() == 'x86_64':
        entry_points = {
            "console_scripts": [
            "ziion = ziion_cli.__main__:main",
            ]
        }
    elif platform.machine() == 'aarch64': 
        entry_points = {
            "console_scripts": [
            "ziion = ziion_cli.__main__:main",
            "solc = ziion_cli.__main__:solc",
            ]
        }
    return entry_points

setup(
    name="ziion",
    author = "Halborn",
    description = ("ziion-cli provides an easy way to manage rust and solc packages for ARM and AMD."),
    version=__version__,
    install_requires=["packaging", "click"],
    packages=["ziion_cli"],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    entry_points=define_entry_points()
)