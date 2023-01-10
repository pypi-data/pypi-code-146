import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-docker",
    "version": "4.0.3",
    "description": "Prebuilt docker Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-docker.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-docker.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_docker",
        "cdktf_cdktf_provider_docker._jsii",
        "cdktf_cdktf_provider_docker.config",
        "cdktf_cdktf_provider_docker.container",
        "cdktf_cdktf_provider_docker.data_docker_image",
        "cdktf_cdktf_provider_docker.data_docker_logs",
        "cdktf_cdktf_provider_docker.data_docker_network",
        "cdktf_cdktf_provider_docker.data_docker_plugin",
        "cdktf_cdktf_provider_docker.data_docker_registry_image",
        "cdktf_cdktf_provider_docker.image",
        "cdktf_cdktf_provider_docker.network",
        "cdktf_cdktf_provider_docker.plugin",
        "cdktf_cdktf_provider_docker.provider",
        "cdktf_cdktf_provider_docker.registry_image",
        "cdktf_cdktf_provider_docker.secret",
        "cdktf_cdktf_provider_docker.service",
        "cdktf_cdktf_provider_docker.tag",
        "cdktf_cdktf_provider_docker.volume"
    ],
    "package_data": {
        "cdktf_cdktf_provider_docker._jsii": [
            "provider-docker@4.0.3.jsii.tgz"
        ],
        "cdktf_cdktf_provider_docker": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "cdktf>=0.14.0, <0.15.0",
        "constructs>=10.0.0, <11.0.0",
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
