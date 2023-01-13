from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='f2r',
    version='2.5.0',
    author='Adam Wegrzynek',
    author_email='adam.wegrzynek@cern.ch',
    url='https://gitlab.cern.ch/AliceO2Group/flp-to-rpm',
    license='GPLv3',
    description='Produces RPMs for FLP packages out of aliBuild ouput',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Environment :: Console',
        'Operating System :: Unix',
        'Development Status :: 4 - Beta'
    ],
    python_requires='>=3.9',
    install_requires=['PyYAML', 'coloredlogs', 's3cmd', 'alibuild'],
    scripts=['f2r'],
    include_package_data=True,
    package_data={
        'flp2rpm': ['after_remove_template.sh', 'after_install_template.sh', 'runtime.slc7.yaml', 'devel.slc7.yaml', 'runtime.slc8.yaml', 'devel.slc8.yaml']
    }
)
