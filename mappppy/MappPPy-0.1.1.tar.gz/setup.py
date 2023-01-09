from setuptools import setup, find_packages

VERSION = '0.1.1'
DESCRIPTION = 'A basic mapping package'
LONG_DESCRIPTION = 'As a basic mapping package. Allows user to plot over top of a dynamic map.'

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
    install_requires=['folium', 'statistics'],
    keywords=['python', 'mapping', 'folium']
)
