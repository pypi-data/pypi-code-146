import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-azuread",
    "version": "4.0.2",
    "description": "Prebuilt azuread Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-azuread.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-azuread.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_azuread",
        "cdktf_cdktf_provider_azuread._jsii",
        "cdktf_cdktf_provider_azuread.administrative_unit",
        "cdktf_cdktf_provider_azuread.administrative_unit_member",
        "cdktf_cdktf_provider_azuread.app_role_assignment",
        "cdktf_cdktf_provider_azuread.application",
        "cdktf_cdktf_provider_azuread.application_certificate",
        "cdktf_cdktf_provider_azuread.application_federated_identity_credential",
        "cdktf_cdktf_provider_azuread.application_password",
        "cdktf_cdktf_provider_azuread.application_pre_authorized",
        "cdktf_cdktf_provider_azuread.claims_mapping_policy",
        "cdktf_cdktf_provider_azuread.conditional_access_policy",
        "cdktf_cdktf_provider_azuread.custom_directory_role",
        "cdktf_cdktf_provider_azuread.data_azuread_administrative_unit",
        "cdktf_cdktf_provider_azuread.data_azuread_application",
        "cdktf_cdktf_provider_azuread.data_azuread_application_published_app_ids",
        "cdktf_cdktf_provider_azuread.data_azuread_application_template",
        "cdktf_cdktf_provider_azuread.data_azuread_client_config",
        "cdktf_cdktf_provider_azuread.data_azuread_directory_object",
        "cdktf_cdktf_provider_azuread.data_azuread_directory_roles",
        "cdktf_cdktf_provider_azuread.data_azuread_domains",
        "cdktf_cdktf_provider_azuread.data_azuread_group",
        "cdktf_cdktf_provider_azuread.data_azuread_groups",
        "cdktf_cdktf_provider_azuread.data_azuread_service_principal",
        "cdktf_cdktf_provider_azuread.data_azuread_service_principals",
        "cdktf_cdktf_provider_azuread.data_azuread_user",
        "cdktf_cdktf_provider_azuread.data_azuread_users",
        "cdktf_cdktf_provider_azuread.directory_role",
        "cdktf_cdktf_provider_azuread.directory_role_assignment",
        "cdktf_cdktf_provider_azuread.directory_role_member",
        "cdktf_cdktf_provider_azuread.group",
        "cdktf_cdktf_provider_azuread.group_member",
        "cdktf_cdktf_provider_azuread.invitation",
        "cdktf_cdktf_provider_azuread.named_location",
        "cdktf_cdktf_provider_azuread.provider",
        "cdktf_cdktf_provider_azuread.service_principal",
        "cdktf_cdktf_provider_azuread.service_principal_certificate",
        "cdktf_cdktf_provider_azuread.service_principal_claims_mapping_policy_assignment",
        "cdktf_cdktf_provider_azuread.service_principal_delegated_permission_grant",
        "cdktf_cdktf_provider_azuread.service_principal_password",
        "cdktf_cdktf_provider_azuread.synchronization_job",
        "cdktf_cdktf_provider_azuread.synchronization_secret",
        "cdktf_cdktf_provider_azuread.user"
    ],
    "package_data": {
        "cdktf_cdktf_provider_azuread._jsii": [
            "provider-azuread@4.0.2.jsii.tgz"
        ],
        "cdktf_cdktf_provider_azuread": [
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
