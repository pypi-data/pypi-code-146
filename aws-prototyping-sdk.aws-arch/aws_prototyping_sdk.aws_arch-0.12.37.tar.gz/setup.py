import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws_prototyping_sdk.aws_arch",
    "version": "0.12.37",
    "description": "@aws-prototyping-sdk/aws-arch",
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
        "aws_prototyping_sdk.aws_arch",
        "aws_prototyping_sdk.aws_arch._jsii",
        "aws_prototyping_sdk.aws_arch.aws_arch",
        "aws_prototyping_sdk.aws_arch.aws_arch.drawio_spec",
        "aws_prototyping_sdk.aws_arch.aws_arch.drawio_spec.aws4",
        "aws_prototyping_sdk.aws_arch.aws_arch.pricing_manifest"
    ],
    "package_data": {
        "aws_prototyping_sdk.aws_arch._jsii": [
            "aws-arch@0.12.37.jsii.tgz"
        ],
        "aws_prototyping_sdk.aws_arch": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
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
