from setuptools import setup, find_packages

setup(
    name='operator-csv-libs',
    version='1.9.18',
    description='Code to manage OLM related CSVs and channels',
    author='bennett-white',
    url='https://github.com/multicloud-ops/operator-csv-libs',
    packages=['operator_csv_libs'],
    install_requires=[
        'pyyaml==6.0',
        'pygithub==1.55',
        'dohq-artifactory==0.7.574 ',
        'requests==2.27.1'
    ]
)
