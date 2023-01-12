from codecs import open
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='defi-marketplace-py',
    description='Python package',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    version='0.1.1',
    author='nevermined.io',
    author_email='root@nevermined.io',
    url='https://github.com/nevermined-io/defi-marketplace-py',
    license='MIT',
    install_requires=['python-dotenv'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    keywords=[
        'finance',
        'analysis',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    python_requires='>=3'
)
