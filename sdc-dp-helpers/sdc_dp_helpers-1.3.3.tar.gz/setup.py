# pylint: disable=invalid-name,line-too-long,pointless-string-statement
"""
    Set up the sdc_helpers package
"""
from distutils.command.sdist import sdist as _sdist
from setuptools import setup


class sdistzip(_sdist):
    """Override sdist to always produce .zip archive"""

    def initialize_options(self):
        _sdist.initialize_options(self)
        self.formats = "zip"


setup(
    name="sdc_dp_helpers",
    packages=[
        "sdc_dp_helpers",
        "sdc_dp_helpers.google_analytics",
        "sdc_dp_helpers.google_analytics_v4",
        "sdc_dp_helpers.google_search_console",
        "sdc_dp_helpers.sailthru",
        "sdc_dp_helpers.azure",
        "sdc_dp_helpers.api_utilities",
        "sdc_dp_helpers.falcon",
        "sdc_dp_helpers.pyspark",
        "sdc_dp_helpers.onesignal",
        "sdc_dp_helpers.xero",
        "sdc_dp_helpers.zoho",
        "sdc_dp_helpers.google_ads",
        "sdc_dp_helpers.facebook",
        "sdc_dp_helpers.google_big_query",
        "sdc_dp_helpers.xml",
        "sdc_dp_helpers.google_knowledge_graph",
    ],
    install_requires=[
        "boto3>=1.17.112",
        "google-api-python-client",
        "httplib2>=0.19.1",
        "oauth2client",
        "numpy",
        "pandas",
        "pyOpenSSL",
        "python-interface",
        "sailthru-client",
        "azure-storage-blob",
        "sdc-helpers==1.6.2",
        "requests>=2.25.1",
        "zcrmsdk==2.0.10",
        "mysql",
        "mysql-connector>=2.2.9",
        "googleads==28.0.0",
        "google-ads==12.0.0",
        "protobuf>=3.20.2",
        "pyxero>=0.9.3",
        "oauth2",
        "python-dateutil>=2.8.1",
        "google-cloud-bigquery",
        "google",
        "google-analytics-data",
        "xmltodict",
    ],
    extras_require={"pyspark": ["pyspark"]},
    cmdclass={"sdist_zip": sdistzip},
    description="A module for developing data pipelines from external api's and on ETL like services",
    version="1.3.3",
    url="http://github.com/RingierIMU/sdc-dataPipeline-helpers",
    author="Ringier South Africa",
    author_email="tools@ringier.co.za",
    keywords=[
        "pip",
        "datapipeline",
        "helpers",
    ],
    download_url="https://github.com/RingierIMU/sdc-global-dataPipeline-helpers/archive/v1.3.3zip",
)
