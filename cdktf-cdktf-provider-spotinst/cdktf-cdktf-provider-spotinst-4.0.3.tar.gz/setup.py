import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-spotinst",
    "version": "4.0.3",
    "description": "Prebuilt spotinst Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-spotinst.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-spotinst.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_spotinst",
        "cdktf_cdktf_provider_spotinst._jsii",
        "cdktf_cdktf_provider_spotinst.data_integration",
        "cdktf_cdktf_provider_spotinst.elastigroup_aws",
        "cdktf_cdktf_provider_spotinst.elastigroup_aws_beanstalk",
        "cdktf_cdktf_provider_spotinst.elastigroup_aws_suspension",
        "cdktf_cdktf_provider_spotinst.elastigroup_azure",
        "cdktf_cdktf_provider_spotinst.elastigroup_azure_v3",
        "cdktf_cdktf_provider_spotinst.elastigroup_gcp",
        "cdktf_cdktf_provider_spotinst.elastigroup_gke",
        "cdktf_cdktf_provider_spotinst.health_check",
        "cdktf_cdktf_provider_spotinst.managed_instance_aws",
        "cdktf_cdktf_provider_spotinst.mrscaler_aws",
        "cdktf_cdktf_provider_spotinst.multai_balancer",
        "cdktf_cdktf_provider_spotinst.multai_deployment",
        "cdktf_cdktf_provider_spotinst.multai_listener",
        "cdktf_cdktf_provider_spotinst.multai_routing_rule",
        "cdktf_cdktf_provider_spotinst.multai_target",
        "cdktf_cdktf_provider_spotinst.multai_target_set",
        "cdktf_cdktf_provider_spotinst.ocean_aks",
        "cdktf_cdktf_provider_spotinst.ocean_aks_virtual_node_group",
        "cdktf_cdktf_provider_spotinst.ocean_aws",
        "cdktf_cdktf_provider_spotinst.ocean_aws_extended_resource_definition",
        "cdktf_cdktf_provider_spotinst.ocean_aws_launch_spec",
        "cdktf_cdktf_provider_spotinst.ocean_ecs",
        "cdktf_cdktf_provider_spotinst.ocean_ecs_launch_spec",
        "cdktf_cdktf_provider_spotinst.ocean_gke_import",
        "cdktf_cdktf_provider_spotinst.ocean_gke_launch_spec",
        "cdktf_cdktf_provider_spotinst.ocean_gke_launch_spec_import",
        "cdktf_cdktf_provider_spotinst.ocean_spark",
        "cdktf_cdktf_provider_spotinst.provider",
        "cdktf_cdktf_provider_spotinst.stateful_node_azure",
        "cdktf_cdktf_provider_spotinst.subscription"
    ],
    "package_data": {
        "cdktf_cdktf_provider_spotinst._jsii": [
            "provider-spotinst@4.0.3.jsii.tgz"
        ],
        "cdktf_cdktf_provider_spotinst": [
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
