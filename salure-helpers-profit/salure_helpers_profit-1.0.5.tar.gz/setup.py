from setuptools import setup


setup(
    name='salure_helpers_profit',
    version='1.0.5',
    description='Profit wrapper from Salure',
    long_description='Profit wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.profit"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1',
        'salure-helpers-salure-functions>=0',
        'aiohttp>=3,<=4',
        'pandas>=1,<=1.35',
        'requests>=2,<=3'
    ],
    zip_safe=False,
)
