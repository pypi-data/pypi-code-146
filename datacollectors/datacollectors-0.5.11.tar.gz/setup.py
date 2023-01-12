from setuptools import setup,find_packages

with open('README.md', 'r') as fh:
    long_description=fh.read()

# import _csv_to_py
#
# _csv_to_py.convert_csv()

from pathlib import Path
py_modules = [f.stem for f in (Path(__file__).parent / 'src').glob('*.py') if f.stem[0] !='_']



setup(

    name='datacollectors',
    version='0.5.11',
    description='datacollectors',
    py_modules=py_modules,
    package_dir={'':'src'},
    install_requires=['tabulate', 'incentivedkutils', 'requests', 'xmltodict'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Torben Franch',
    author_email='torben@franch.eu',
    include_package_data=True,
    packages=find_packages(exclude=['_*']),

)