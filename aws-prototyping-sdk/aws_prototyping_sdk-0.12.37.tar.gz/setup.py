import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws_prototyping_sdk",
    "version": "0.12.37",
    "description": "aws-prototyping-sdk",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/aws-prototyping-sdk",
    "long_description_content_type": "text/markdown",
    "author": "AWS APJ COPE<apj-cope@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws/aws-prototyping-sdk"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_prototyping_sdk",
        "aws_prototyping_sdk._jsii",
        "aws_prototyping_sdk.nx_monorepo",
        "aws_prototyping_sdk.pdk_nag",
        "aws_prototyping_sdk.pipeline"
    ],
    "package_data": {
        "aws_prototyping_sdk._jsii": [
            "aws-prototyping-sdk@0.12.37.jsii.tgz"
        ],
        "aws_prototyping_sdk": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.53.0, <3.0.0",
        "cdk-nag>=2.21.4, <3.0.0",
        "constructs>=10.1.162, <11.0.0",
        "jsii>=1.71.0, <2.0.0",
        "projen>=0.65.26, <0.66.0",
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
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
