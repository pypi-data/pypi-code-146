from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: MacOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='prettycode',
    version='0.0.1',
    description='A simple library to generate pretty pseudo-random verification codes',
    long_description=open('README.txt').read(),
    url='',
    author='Nikolai Suanov',
    author_email='suanwow@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='verification codes',
    packages=find_packages(),
    install_requires=['']
)