import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdklabs.codepipeline-extensions",
    "version": "0.0.70",
    "description": "This project is for use in the workshop DOP 401: Get better at building AWS CDK constructs.",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-codepipeline-extensions.git",
    "long_description_content_type": "text/markdown",
    "author": "Kendra Neil<kneil@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-codepipeline-extensions.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk.codepipeline_extensions",
        "cdk.codepipeline_extensions._jsii"
    ],
    "package_data": {
        "cdk.codepipeline_extensions._jsii": [
            "cdk-codepipeline-extensions@0.0.70.jsii.tgz"
        ],
        "cdk.codepipeline_extensions": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.50.0, <3.0.0",
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
