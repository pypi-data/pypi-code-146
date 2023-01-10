from setuptools import setup


setup(
    name='salure_helpers_all_solutions',
    version='1.0.2',
    description='All Solutions wrapper from Salure',
    long_description='All Solutions wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.all_solutions"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1',
        'requests>=2,<=3',
        'cryptography>=38,<=38',
    ],
    zip_safe=False,
)