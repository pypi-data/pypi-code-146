import setuptools
from distutils.util import convert_path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

ns = {}
ver_path = convert_path('deepdriver/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), ns)

setuptools.setup(
    name="deepdriver",
    version=ns['__version__'],
    author="bokchi",
    author_email="molamola.bokchi@gmail.com",
    description="deepdriver experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bokchi.com",
    project_urls={
        "bokchi git hub": "https://github.com/molabokchi",
    },
    install_requires=[
        "wheel",
        "assertpy",
        "grpcio",
        "grpcio-tools",
        "numpy",
        "pandas",
        "Pillow",
        "plotly",
        "psutil",
        "pynvml",
        "requests",
        "optuna",
        "psycopg2"
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"."},
    packages=["deepdriver","deepdriver.sdk","deepdriver.intergration","deepdriver.intergration.keras","deepdriver.sdk.chart","deepdriver.sdk.data_types","deepdriver.sdk.interface","deepdriver.sdk.lib",""],
    python_requires=">=3.6"
)