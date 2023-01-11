from setuptools import setup
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='spectra2rgb',
    version='1.0.0',
    description='Converts multi-spectrum cube to RGB image',
    author='Shabbir Nuruddin Bawaji',
    author_email='bawaji94@gmail.com',
    url='https://github.com/bawaji94/spectra2rgb',
    packages=['spectra2rgb'],
    install_requires=['numpy>=1.3.0'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
