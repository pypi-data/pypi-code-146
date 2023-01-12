from os import path
import io
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import unittest.mock
    has_mock = True
except ImportError:
    has_mock = False

__author__ = 'Charan <firstmodified@gmail.com>'
__version__ = '1.0.1'

packages = [
    'insta_cs',
    'insta_cs.endpoints',
    'insta_web_cs'
]
test_reqs = [] if has_mock else ['mock']

with io.open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='insta_cs',
    version=__version__,
    author='Charan',
    author_email='firstmodified@gmail.com',
    license='MIT',
    # url='https://github.com/',
    install_requires=[],
    test_requires=test_reqs,
    keywords='insta_cs instagram',
    description='A client interface for the Instagram automation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=packages,
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
