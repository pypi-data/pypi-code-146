import os
from setuptools import setup, find_packages

setup(
    name='sonotoria',
    version=os.environ['CI_COMMIT_BRANCH'],
    description='Templating utilities',
    long_description=open('README.md').read()+'\n\n\n'+open('CHANGELOG.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/neomyte/sonotoria',
    author='Emmanuel Pluot',
    author_email='emmanuel.pluot@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'jinja2',
        'python-benedict'
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: MIT License',
    ]
)