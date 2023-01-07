import pathlib
from setuptools import find_packages, setup

setup(
    name = 'ERlib',
    version = '1',
    description = 'Librería para imprimir tablas',
    long_description = (pathlib.Path(__file__).parent / "README.md").read_text(encoding='utf-8'),
    long_description_content_type = "text/markdown",
    author = 'Erwin Martínez Pérez',
    author_email = 'erwinmartinezperez@gmail.com',
    url = 'https://github.com/ERwiin21MP',
    license = 'GPLv3',
    packages = find_packages(),
    include_package_data = True
)