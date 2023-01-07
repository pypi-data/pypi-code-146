from setuptools import setup


def readme():
    with open('README.md', 'r') as file:
        return file.read()


setup(
    name='colorer',
    version='1.0.2',
    author='ALhorm',
    author_email='gladkoam@gmail.com',
    description='A simple and handy library for coloring strings.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/ALhorm/colorer',
    packages=['colorer'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.0'
)
