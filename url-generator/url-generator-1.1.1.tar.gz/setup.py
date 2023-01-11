from setuptools import setup

setup(
    name='url-generator',
    description="Universal URL generator.",
    version='1.1.1',
    license='Apache',
    author='Heureka.cz',
    author_email='vyvoj@heureka.cz',
    url='https://github.com/heureka/py-url-generator',
    packages=['url_generator'],
    long_description=open('./README.md', 'r').read(),
    long_description_content_type='text/markdown',
)
