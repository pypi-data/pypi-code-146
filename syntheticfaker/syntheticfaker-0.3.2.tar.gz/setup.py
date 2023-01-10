from distutils.core import setup


files = ["syntheticfaker/data/*.yaml", "syntheticfaker/*"]


setup(
    name='syntheticfaker',
    version='0.3.2',    
    description='A Synthetic Data Generation Python package',
    url='https://github.com/dominic12/synthetic_faker',
    author="Ninad Magdum",
    author_email="ninadmagdum13@gmail.com",
    license='BSD 2-clause',
    packages = ['syntheticfaker'],
    package_data = {'package' : files },
    include_package_data=True,
    install_requires=['faker',
                      'pandas'                    
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',      
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",  
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)