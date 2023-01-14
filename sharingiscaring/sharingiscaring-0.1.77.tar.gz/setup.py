from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='sharingiscaring',
    version='0.1.77',
    author='Sander de Ruiter',
    author_email='sdr@concordium-explorer.nl',
    description='Shared code for Concordium Explorer (Bot)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sderuiter/sharingiscaring',
    project_urls={
    },
    license='MIT',
    packages=find_packages(),
    install_requires=['rich', 'python-dateutil', 
        'base58', 'pysha3', 'pytest', 'pydantic', 
        'pymongo', 'requests', 'apprise', 'py-graphql-client'],
)