import os

from setuptools import find_packages, setup
from pathlib import Path

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="dnoticias_backoffice",
    version='1.2.0a2',
    url="https://www.dnoticias.pt/",
    author="Pedro Mendes",
    author_email="pedro.trabalho.uma@gmail.com",
    maintainer="Nélson Gomes",
    maintainer_email="ngoncalves@dnoticias.pt",
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'django',
        'django-flags',
        'djangorestframework',
        'django-dnoticias-tables',
        'slippers',
    ],
    include_package_data=True,
    packages=find_packages(),
    data_files=[('dnoticias_backoffice', [str(path) for path in Path('./dnoticias_backoffice/templates').rglob('*')  if os.path.isfile(str(path))])]
)
