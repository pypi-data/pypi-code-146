import setuptools

setuptools.setup(
    name='pub_sub_to_bigquery',
    version='0.1',
    description='Dependencies',
    install_requires=[
        "prophet",
        "dynaconf",
        "txp[cloud]"
    ],
    packages=setuptools.find_packages()
)
