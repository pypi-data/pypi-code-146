from setuptools import setup, find_packages

setup(
    name='velait_api',
    version='0.0.10',
    license='LICENSE.md',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    optional_requires={
        'django': ['django', 'djangorestframework', 'djangorestframework-camel-case'],
        'fastapi': ['fastapi', 'sqlalchemy', 'py-assimilator', 'dependency-injector', 'aiohttp'],
    },
)
