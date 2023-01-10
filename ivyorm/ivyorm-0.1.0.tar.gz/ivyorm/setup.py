from setuptools import setup, find_packages

requires = [
    'psycopg2',
    'jsonschema'
]

setup(
    name='ivypy',
    version='0.1',
    description='Ivy for Python',
    author='James Randell',
    author_email='jamesrandell@me.com',
    keywords='Ivy Python',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)