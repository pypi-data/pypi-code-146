import setuptools

setuptools.setup(
    name='batch_signals_to_bigquery',
    version='0.1',
    description='Dependencies',
    install_requires=[
        "dynaconf",
        "txp[cloud]"
    ],
    packages=setuptools.find_packages()
)
