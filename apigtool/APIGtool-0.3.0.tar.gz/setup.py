from setuptools import setup
setup(
    name="APIGtool",
    version='0.3.0',
    packages=['apigtool'],
    description='Collection of APIG Utilities',
    author='Chuck Muckamuck',
    author_email='chuck.muckamuck@gmail.com',
    install_requires=[
        "boto3>=1.7",
        "Click>=6.7",
        "pymongo>=3.6",
        "tabulate>=0.8"
    ],
    entry_points="""
        [console_scripts]
        apigtool=apigtool.command:cli
    """
)
