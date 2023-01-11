from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='consumetpy',
    version='0.1.0',
    author='Jawad',
    author_email='evrynoiseatonce@gmail.com',
    description='A wrapper for the Consumet API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/notjawad/consumet-py',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
