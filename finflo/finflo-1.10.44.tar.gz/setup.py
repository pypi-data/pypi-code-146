from setuptools import setup, find_packages


# read from README.RST
def readme():
    with open('readme.md') as f:
        return f.read()


setup(
    name='finflo',
    author= "AnandRaj",
    long_description=readme(),
    long_description_content_type='text/markdown'
)