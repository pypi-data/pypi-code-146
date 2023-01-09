from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='keap_flask',
    version='0.5.0',
    description='A Rest Client For Flask applications',
    author='will sexton',
    author_email='will@theapiguys.com',
    url='https://github.com/codinlikewilly/keap_flask',
    readme = "README.md",
    license='BSD 2-clause',
    packages=['keap_flask'],
    install_requires=['Flask',
                      'AuthLib',
                      'python-dateutil',
                      'requests'
                      ],

    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
    long_description=long_description
)
