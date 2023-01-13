from setuptools import setup

setup(
    name='simassis',
    version='0.1.5',
    description='A python Package for MD calculations in solids',
    author='Marcin Krynski',
    author_email='marcin.krynski@pw.edu.pl',
    url='https://github.com/marcinkrynskipw/simassis',
    license='BSD 2-clause',
    packages=['simassis'],
    install_requires=[
                      'numpy',
                      'scipy',   
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
