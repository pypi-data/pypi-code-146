from setuptools import setup
from os.path import join, dirname


setup(name='myapiframework',
      version='1.0',
      description='eazy python framework',
      long_description=open(join(dirname(__file__), 'README.md')).read(),
      long_description_content_type = "text/markdown",
      install_requires = ['parse', 'gunicorn'],
      packages=['myapiframework'],
      author='Barashov',
      author_email='barashovmisha@gmail.com',
      url='https://github.com/Barashov/Myapi'
)

