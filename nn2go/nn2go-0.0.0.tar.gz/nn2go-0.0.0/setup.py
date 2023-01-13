# Module imports
from setuptools import setup

# Arguments
version = "0.0.0"
python_version = ">=3.10"

with open("README.md", "r") as fh:
    long_description = fh.read()

# Run setup function
setup(
    name = 'nn2go',
    version = version,
    description = 'Pre-trained neural networks ready for deployment.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'nn2go team',
    author_email = 'jordan.welsman@hotmail.co.uk',
    url = 'https://github.com/nn2go/nn',
    py_modules = ["__init__"],
    classifiers = [
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License'
    ],
    package_dir = {'': 'nn2go'},
    install_requires = [
        "jutils"
    ]
)