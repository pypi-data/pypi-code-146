from distutils.core import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory /"syntheticfaker/README.md").read_text()


files = ["syntheticfaker/data/*.yaml", "syntheticfaker/*"]


setup(
    name='syntheticfaker',
    version='1.0.1',    
    description='A Synthetic Data Generation Python package',
    long_description=long_description,
    long_description_content_type='text/markdown',
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