import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cloudy-with-a-chance-of-meatballs.cdk-lambda-token-authorizer-jwt",
    "version": "0.1.9",
    "description": "Add a lambda function to your aws-rest-api-gateway which can be used as a token authorizer",
    "license": "MIT",
    "url": "https://github.com/cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt.git",
    "long_description_content_type": "text/markdown",
    "author": "cfuerst<c.fuerst@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cloudy-with-a-chance-of-meatballs/cdk-lambda-token-authorizer-jwt.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cloudy_with_a_chance_of_meatballs_cdk_lambda_token_authorizer_jwt",
        "cloudy_with_a_chance_of_meatballs_cdk_lambda_token_authorizer_jwt._jsii"
    ],
    "package_data": {
        "cloudy_with_a_chance_of_meatballs_cdk_lambda_token_authorizer_jwt._jsii": [
            "cdk-lambda-token-authorizer-jwt@0.1.9.jsii.tgz"
        ],
        "cloudy_with_a_chance_of_meatballs_cdk_lambda_token_authorizer_jwt": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.5.0, <3.0.0",
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
