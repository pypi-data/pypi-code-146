import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "streamlink-serverless",
    "version": "0.0.47",
    "description": "Streamlink as a Service",
    "license": "MIT",
    "url": "https://github.com/mrgrain/streamlink-serverless.git",
    "long_description_content_type": "text/markdown",
    "author": "Momo Kornher<mail@moritzkornher.de>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mrgrain/streamlink-serverless.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "streamlink_serverless",
        "streamlink_serverless._jsii"
    ],
    "package_data": {
        "streamlink_serverless._jsii": [
            "streamlink-serverless@0.0.47.jsii.tgz"
        ],
        "streamlink_serverless": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
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
