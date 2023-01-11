import aiohttp

DEFAULT_ENDPOINT_URL = "{{cookiecutter.servers|first}}"


async def gather(hub):
    """
    Authenticate with a username and password to the given endpoint url.
    Any extra parameters will be saved as part of the profile.

    Example:

    .. code-block:: sls

        {{cookiecutter.service_name}}.basic_auth:
          profile_name:
            username: my_user
            password: my_token
            endpoint_url: {{cookiecutter.servers|join('|')}}
    """
    sub_profiles = {}
    for profile, ctx in hub.acct.PROFILES.get(
        "{{cookiecutter.service_name}}.basic_auth", {}
    ).items():
        sub_profiles[profile] = dict(
            endpoint_url=ctx.pop("endpoint_url", DEFAULT_ENDPOINT_URL),
            auth=aiohttp.BasicAuth(ctx.pop("username"), ctx.pop("password")),
            **ctx
        )

    return sub_profiles
