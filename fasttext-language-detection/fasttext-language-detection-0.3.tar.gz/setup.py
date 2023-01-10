import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='fasttext-language-detection',
    version='0.3',
    packages=['test', 'langdetection'],
    url='https://github.com/lang-ai/fasttext-language-detection',
    license='MIT',
    author='Alberto Ezpondaburu',
    author_email='aezpondaburu@lang.ai ',
    description='Language detection wrapper with fasttext',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=['fasttext==0.9.2', 'pytest==7.2.0', 'logger==1.4'],
    keywords=['language detection', 'language identification', 'fasttext'],
    classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
)
