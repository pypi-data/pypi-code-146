from setuptools import setup, find_packages

import deap_misl

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='deap_misl',
    version=deap_misl.__version__,
    description='DEAP additional tooklit by MISL',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/D-HISL/deap_misl',
    author='junjis0203',
    author_email='junjis0203@gmail.com',
    packages=find_packages(exclude=['examples']),
    platforms=['any'],
    keywords=['evolutionary algorithms', 'genetic algorithms', 'ga'],
    license='LGPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],
    install_requires=['deap'],
)
