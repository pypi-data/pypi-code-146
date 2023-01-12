from setuptools import setup, find_packages

setup(
    name="FMSHProjectGenerator",
    install_requires=['Jinja2>=3.0.1', 'ruamel.yaml>=0.17.9', 'xmltodict>=0.12.0', 'chardet2>=2.0.3'],
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={
        "": ["templates/*.*", "assets/*.*", "chips/*.*"],
    }
)
