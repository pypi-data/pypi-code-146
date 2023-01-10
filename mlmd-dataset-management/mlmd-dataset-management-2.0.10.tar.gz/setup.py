from setuptools import setup, find_packages
from distutils.dir_util import remove_tree
# import glob
# remove_tree(['dist']) 

setup(
    name="mlmd-dataset-management",
    version="2.0.10",
    description="MLMD Dataset Management",
    long_description="MLMD Dataset Management",
    long_description_content_type="text/markdown",
    url="",
    author="Thinh Nguyen",
    author_email="nguyenlongthinh@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["azure-storage-blob","requests","ml-metadata==1.0.0","python-dotenv","google-cloud-storage","mysql-connector-python==8.0.12", "google-cloud-secret-manager", "google-api-python-client", "protobuf==3.20.1"],
    entry_points = {
        'console_scripts': ['dm=cli.dataset_manager:main']
    }

)