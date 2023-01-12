async def gather(hub, profiles):
    """
    load k8s profiles from credential files

    Example:
    .. code-block:: yaml

        k8s:
          profile_name:
            kube_config_path: '~/.kube/config'
            context: kubernetes-admin
    """
    sub_profiles = {}
    for profile, ctx in profiles.get("k8s", {}).items():
        sub_profiles[profile] = ctx

    k8s_profile = (hub.OPT.get("idem") or {}).get("acct_profile")
    if k8s_profile not in sub_profiles:
        sub_profiles[k8s_profile] = {"": ""}

    return sub_profiles
