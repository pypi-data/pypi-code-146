"""cookiecutter distutils configuration."""
from pathlib import Path
from setuptools import setup


with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = Path('requirements.txt').read_text()
version = Path('version').read_text()

setup(
    name='midi_etl',
    version=version,
    description=(
        'Midi ETL pipelines implemented with dagster + dbt'
    ),
    long_description=readme,
    long_description_content_type='text/markdown',
    # author='Audrey Feldroy',
    # author_email='audreyr@gmail.com',
    # url='https://github.com/cookiecutter/cookiecutter',
    packages=['midi_etl'],
    package_dir={'midi_etl': 'midi_etl'},
    include_package_data=True,
    python_requires='>=3.10',
    install_requires=requirements,
)