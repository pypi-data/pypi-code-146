from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='flask_servicefusion',
    version='0.6.0',
    description='A servicefusion Rest Client For Flask applications',
    author='will sexton',
    author_email='will@theapiguys.com',
    url='https://bitbucket.org/will_sexton/flask_servicefusion/src/master/',
    readme="README.md",
    license='BSD 2-clause',
    packages=find_packages(),
    install_requires=['Flask',
                      'AuthLib',
                      'python-dateutil',
                      'requests'
                      ],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown"

)
