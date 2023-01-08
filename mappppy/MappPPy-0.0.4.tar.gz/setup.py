from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'A basic mapping package'
LONG_DESCRIPTION = 'Something'

# Setting up
setup(
    name="MappPPy",
    version=VERSION,
    author="Gabriel Tower",
    author_email="<gmtower1@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/KilroyWasHere-cs-j/MapPy.git',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['folium', 'statistics', 'webbrowser'],
    keywords=['python', 'mapping', 'folium']
)
