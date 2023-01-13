import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-extensions",
    "version": "0.0.42",
    "description": "cdk-extensions",
    "license": "Apache-2.0",
    "url": "https://github.com/vibe-io/cdk-extensions.git",
    "long_description_content_type": "text/markdown",
    "author": "Kevin Lucas<kevinluc08@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/vibe-io/cdk-extensions.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_extensions",
        "cdk_extensions._jsii",
        "cdk_extensions.asserts",
        "cdk_extensions.athena",
        "cdk_extensions.core",
        "cdk_extensions.ec2",
        "cdk_extensions.eks_patterns",
        "cdk_extensions.glue",
        "cdk_extensions.glue_tables",
        "cdk_extensions.k8s_aws",
        "cdk_extensions.kinesis_firehose",
        "cdk_extensions.ram",
        "cdk_extensions.rds",
        "cdk_extensions.route53",
        "cdk_extensions.s3_buckets",
        "cdk_extensions.sso",
        "cdk_extensions.stacks"
    ],
    "package_data": {
        "cdk_extensions._jsii": [
            "cdk-extensions@0.0.42.jsii.tgz"
        ],
        "cdk_extensions": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.59.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.69.0, <2.0.0",
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
    "scripts": [
        "src/cdk_extensions/_jsii/bin/init-aws.sh"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
