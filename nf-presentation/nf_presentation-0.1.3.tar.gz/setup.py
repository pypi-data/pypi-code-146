from setuptools import setup, find_packages
from pathlib import Path

with open('requirements.txt','r') as f:
    requirements=f.readlines()

this_directory=Path(__file__).parent
long_description=(this_directory / 'README.MD').read_text(encoding='utf8')


setup(
    name='nf_presentation',
    version='0.1.3',
    author='Dmitriy Frolenko',
    author_email='orangefrol@gmail.com',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=requirements, # лол без этой строчки он ругался на README.MD
    dependency_links=['http://www.lfd.uci.edu/~gohlke/'], # here lies windows packages
    url='https://github.com/thefrol/nanofootball-presentation-maker',
    long_description=long_description,
    long_description_content_type='text/markdown; variant=GFM',
    license="MIT",
    python_requires='>3.7.0',
    package_data={
        'nf_presentation':['*.png','*.json']
    }

)