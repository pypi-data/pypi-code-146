from setuptools import setup,find_packages

setup(
    name='dtopia',
    version='1.1.15',
    description='Dtopia Discord Tools',
    author='Toxbic',
    author_email='your@email.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'websockets',
        'colorama',
    ],
)