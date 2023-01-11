import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-cloudflare",
    "version": "4.0.4",
    "description": "Prebuilt cloudflare Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-cloudflare.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-cloudflare.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_cloudflare",
        "cdktf_cdktf_provider_cloudflare._jsii",
        "cdktf_cdktf_provider_cloudflare.access_application",
        "cdktf_cdktf_provider_cloudflare.access_bookmark",
        "cdktf_cdktf_provider_cloudflare.access_ca_certificate",
        "cdktf_cdktf_provider_cloudflare.access_group",
        "cdktf_cdktf_provider_cloudflare.access_identity_provider",
        "cdktf_cdktf_provider_cloudflare.access_keys_configuration",
        "cdktf_cdktf_provider_cloudflare.access_mutual_tls_certificate",
        "cdktf_cdktf_provider_cloudflare.access_organization",
        "cdktf_cdktf_provider_cloudflare.access_policy",
        "cdktf_cdktf_provider_cloudflare.access_rule",
        "cdktf_cdktf_provider_cloudflare.access_service_token",
        "cdktf_cdktf_provider_cloudflare.account",
        "cdktf_cdktf_provider_cloudflare.account_member",
        "cdktf_cdktf_provider_cloudflare.api_shield",
        "cdktf_cdktf_provider_cloudflare.api_token",
        "cdktf_cdktf_provider_cloudflare.argo",
        "cdktf_cdktf_provider_cloudflare.argo_tunnel",
        "cdktf_cdktf_provider_cloudflare.authenticated_origin_pulls",
        "cdktf_cdktf_provider_cloudflare.authenticated_origin_pulls_certificate",
        "cdktf_cdktf_provider_cloudflare.byo_ip_prefix",
        "cdktf_cdktf_provider_cloudflare.certificate_pack",
        "cdktf_cdktf_provider_cloudflare.custom_hostname",
        "cdktf_cdktf_provider_cloudflare.custom_hostname_fallback_origin",
        "cdktf_cdktf_provider_cloudflare.custom_pages",
        "cdktf_cdktf_provider_cloudflare.custom_ssl",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_access_identity_provider",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_account_roles",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_accounts",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_api_token_permission_groups",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_devices",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_ip_ranges",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_load_balancer_pools",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_origin_ca_root_certificate",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_record",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_waf_groups",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_waf_packages",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_waf_rules",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_zone",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_zone_dnssec",
        "cdktf_cdktf_provider_cloudflare.data_cloudflare_zones",
        "cdktf_cdktf_provider_cloudflare.device_managed_networks",
        "cdktf_cdktf_provider_cloudflare.device_policy_certificates",
        "cdktf_cdktf_provider_cloudflare.device_posture_integration",
        "cdktf_cdktf_provider_cloudflare.device_posture_rule",
        "cdktf_cdktf_provider_cloudflare.device_settings_policy",
        "cdktf_cdktf_provider_cloudflare.dlp_profile",
        "cdktf_cdktf_provider_cloudflare.email_routing_address",
        "cdktf_cdktf_provider_cloudflare.email_routing_catch_all",
        "cdktf_cdktf_provider_cloudflare.email_routing_rule",
        "cdktf_cdktf_provider_cloudflare.email_routing_settings",
        "cdktf_cdktf_provider_cloudflare.fallback_domain",
        "cdktf_cdktf_provider_cloudflare.filter",
        "cdktf_cdktf_provider_cloudflare.firewall_rule",
        "cdktf_cdktf_provider_cloudflare.gre_tunnel",
        "cdktf_cdktf_provider_cloudflare.healthcheck",
        "cdktf_cdktf_provider_cloudflare.ip_list",
        "cdktf_cdktf_provider_cloudflare.ipsec_tunnel",
        "cdktf_cdktf_provider_cloudflare.list",
        "cdktf_cdktf_provider_cloudflare.load_balancer",
        "cdktf_cdktf_provider_cloudflare.load_balancer_monitor",
        "cdktf_cdktf_provider_cloudflare.load_balancer_pool",
        "cdktf_cdktf_provider_cloudflare.logpull_retention",
        "cdktf_cdktf_provider_cloudflare.logpush_job",
        "cdktf_cdktf_provider_cloudflare.logpush_ownership_challenge",
        "cdktf_cdktf_provider_cloudflare.magic_firewall_ruleset",
        "cdktf_cdktf_provider_cloudflare.managed_headers",
        "cdktf_cdktf_provider_cloudflare.notification_policy",
        "cdktf_cdktf_provider_cloudflare.notification_policy_webhooks",
        "cdktf_cdktf_provider_cloudflare.origin_ca_certificate",
        "cdktf_cdktf_provider_cloudflare.page_rule",
        "cdktf_cdktf_provider_cloudflare.pages_domain",
        "cdktf_cdktf_provider_cloudflare.pages_project",
        "cdktf_cdktf_provider_cloudflare.provider",
        "cdktf_cdktf_provider_cloudflare.rate_limit",
        "cdktf_cdktf_provider_cloudflare.record",
        "cdktf_cdktf_provider_cloudflare.ruleset",
        "cdktf_cdktf_provider_cloudflare.spectrum_application",
        "cdktf_cdktf_provider_cloudflare.split_tunnel",
        "cdktf_cdktf_provider_cloudflare.static_route",
        "cdktf_cdktf_provider_cloudflare.teams_account",
        "cdktf_cdktf_provider_cloudflare.teams_list",
        "cdktf_cdktf_provider_cloudflare.teams_location",
        "cdktf_cdktf_provider_cloudflare.teams_proxy_endpoint",
        "cdktf_cdktf_provider_cloudflare.teams_rule",
        "cdktf_cdktf_provider_cloudflare.tiered_cache",
        "cdktf_cdktf_provider_cloudflare.total_tls",
        "cdktf_cdktf_provider_cloudflare.tunnel_config",
        "cdktf_cdktf_provider_cloudflare.tunnel_route",
        "cdktf_cdktf_provider_cloudflare.tunnel_virtual_network",
        "cdktf_cdktf_provider_cloudflare.url_normalization_settings",
        "cdktf_cdktf_provider_cloudflare.user_agent_blocking_rule",
        "cdktf_cdktf_provider_cloudflare.waf_group",
        "cdktf_cdktf_provider_cloudflare.waf_override",
        "cdktf_cdktf_provider_cloudflare.waf_package",
        "cdktf_cdktf_provider_cloudflare.waf_rule",
        "cdktf_cdktf_provider_cloudflare.waiting_room",
        "cdktf_cdktf_provider_cloudflare.waiting_room_event",
        "cdktf_cdktf_provider_cloudflare.waiting_room_rules",
        "cdktf_cdktf_provider_cloudflare.web3_hostname",
        "cdktf_cdktf_provider_cloudflare.worker_cron_trigger",
        "cdktf_cdktf_provider_cloudflare.worker_route",
        "cdktf_cdktf_provider_cloudflare.worker_script",
        "cdktf_cdktf_provider_cloudflare.workers_kv",
        "cdktf_cdktf_provider_cloudflare.workers_kv_namespace",
        "cdktf_cdktf_provider_cloudflare.zone",
        "cdktf_cdktf_provider_cloudflare.zone_cache_variants",
        "cdktf_cdktf_provider_cloudflare.zone_dnssec",
        "cdktf_cdktf_provider_cloudflare.zone_lockdown",
        "cdktf_cdktf_provider_cloudflare.zone_settings_override"
    ],
    "package_data": {
        "cdktf_cdktf_provider_cloudflare._jsii": [
            "provider-cloudflare@4.0.4.jsii.tgz"
        ],
        "cdktf_cdktf_provider_cloudflare": [
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
