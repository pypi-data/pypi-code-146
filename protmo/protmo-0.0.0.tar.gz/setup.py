import pathlib
from setuptools import setup, find_packages
from distutils.core import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='protmo',
    url='',
    version='0.0.0',
    author='Thomas Deniffel',
    author_email='tdeniffel@gmail.com',
    packages=['protmo'], # find_packages(),
    license='',
    install_requires=[
        'grpcio-tools'
        'pymongo'
        'python-keycloak'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    description='',
    long_description='', # README
    long_description_content_type="text/markdown",
    python_requires='>=3',
    include_package_data=True,
    entry_points={
    }
)