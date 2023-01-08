from setuptools import setup, find_packages

# Read the contents of the README.md file
from pathlib import Path
current_directory = Path(__file__).parent
long_description = (current_directory/'README.md').read_text()

setup(
    name = 'genelib',
    version = '0.0.1',
    packages = find_packages(),

    # Dependency
    install_requires = [
        'requests',
    ],

    # Metadata
    author = 'Yan Kuang',
    author_email = 'YTKme@Outlook.com',
    description = 'Genetic Library.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license = 'MIT License',
    keywords = 'genetic genelib'
)