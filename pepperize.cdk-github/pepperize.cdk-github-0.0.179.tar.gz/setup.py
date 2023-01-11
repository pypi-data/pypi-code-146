import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "pepperize.cdk-github",
    "version": "0.0.179",
    "description": "Manage GitHub resources like repositories, teams, members, integrations and workflows with the AWS CDK as Custom Resources in CloudFormation with [cdk-github](https://github.com/pepperize/cdk-github).",
    "license": "MIT",
    "url": "https://github.com/pepperize/cdk-github.git",
    "long_description_content_type": "text/markdown",
    "author": "Patrick Florek<patrick.florek@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/pepperize/cdk-github.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "pepperize_cdk_github",
        "pepperize_cdk_github._jsii"
    ],
    "package_data": {
        "pepperize_cdk_github._jsii": [
            "cdk-github@0.0.179.jsii.tgz"
        ],
        "pepperize_cdk_github": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.48.0, <3.0.0",
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
