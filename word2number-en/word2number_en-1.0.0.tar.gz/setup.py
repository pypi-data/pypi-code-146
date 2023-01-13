import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def open_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))

setup(
  name = 'word2number_en',
  packages = ['word2number_en'],  # this must be the same as the name above
  version = '1.0.0',
  license=open('LICENSE.txt').read(),
  description = 'Convert number words (eg. twenty one) to numeric digits (21)',
  author = 'Neuri',
  author_email = 'support@neuri.ai',
  url = 'https://github.com/Neuri-ai/w2n_en',  # use the URL to the github repo
  keywords = ['numbers', 'convert', 'words', 'english'],  # arbitrary keywords
  classifiers = [
      'Intended Audience :: Developers',
      'Programming Language :: Python'
  ],
  long_description=open_file('README.rst').read(),
  long_description_content_type="text/markdown",
)