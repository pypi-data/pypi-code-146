import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-slack-chatbot",
    "version": "1.0.78",
    "description": "cdk-slack-chatbot",
    "license": "Apache-2.0",
    "url": "https://github.com/lvthillo/cdk-slack-chatbot.git",
    "long_description_content_type": "text/markdown",
    "author": "Lorenz Vanthillo<lorenz.vanthillo@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/lvthillo/cdk-slack-chatbot.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_slack_chatbot",
        "cdk_slack_chatbot._jsii"
    ],
    "package_data": {
        "cdk_slack_chatbot._jsii": [
            "cdk-slack-chatbot@1.0.78.jsii.tgz"
        ],
        "cdk_slack_chatbot": [
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
