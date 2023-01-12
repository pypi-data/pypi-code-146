from setuptools import setup, find_namespace_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='agconnect',
    version = '1.2.0.300',
    packages=find_namespace_packages(include=['agconnect.*'], exclude=[
        'agconnect.auth_server.test',
        'agconnect.common_server.test',
        'agconnect.cloud_function.test',
        'agconnect.database_server.test']),
    long_description=long_description,
    long_description_content_type='text/markdown'
)
