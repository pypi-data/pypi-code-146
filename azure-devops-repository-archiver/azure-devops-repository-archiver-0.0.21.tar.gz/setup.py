import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "azure-devops-repository-archiver",
    "version": "0.0.21",
    "description": "azure-devops-repository-archiver",
    "license": "Apache-2.0",
    "url": "https://github.com/stefanfreitag/azure_s3_repository_archiver.git",
    "long_description_content_type": "text/markdown",
    "author": "Stefan Freitag<stefan.freitag@udo.edu>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/stefanfreitag/azure_s3_repository_archiver.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "azure_devops_repository_archiver",
        "azure_devops_repository_archiver._jsii"
    ],
    "package_data": {
        "azure_devops_repository_archiver._jsii": [
            "azure-devops-repository-archiver@0.0.21.jsii.tgz"
        ],
        "azure_devops_repository_archiver": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.59.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.73.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
