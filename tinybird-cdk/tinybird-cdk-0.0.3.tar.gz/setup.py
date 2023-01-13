from setuptools import setup

setup(
    name='tinybird-cdk',
    version='0.0.3',
    description="Tinybird's Connector Development Kit.",
    long_description='This package is under active development and currently meant for internal use only.',
    long_description_content_type='text/markdown',
    author='tinybird.co',
    author_email="support@tinybird.co",
    python_requires='>=3.8, <3.11',
    install_requires=[
        'boto3',
        'python-dateutil',
        'faker',
        'google-cloud-bigquery',
        'google-cloud-storage',
        'humanize',
        'httpx[http2]',
        'kinesis-python',
        'mysql-connector-python',
        'ndjson',
        'psycopg2-binary',
        'snowflake-connector-python',
    ],
    package_dir={"tinybird_cdk": "tinybird_cdk/"},
)
