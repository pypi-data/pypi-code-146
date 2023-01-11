from setuptools import setup, find_packages

VERSION: str = '0.4.5'

setup(
    name='apna-experiment-sdk',
    # packages=['apna_python_experiment_sdk'],
    packages=find_packages(),
    description='This is the SDK for fetching variants in experiments and tracking it to sinks like Bigquery and Mixpanel.',
    version=VERSION,
    url='',
    author='Deval Sethi',
    author_email='devals@apna.co',
    keywords=['pip', 'experiment'],
    install_requires=[
        'rudder-sdk-python>=1.0.0b1',
        'UnleashClient>=4.4.1',
        'python-dotenv>=0.19.1',
        'mixpanel>=4.9.0'
    ]
)
