HTTP_REQUEST = """
return await hub.tool.http.session.request(
    ctx,
    method="{{{{ function.hardcoded.method }}}}",
    path=ctx.acct.endpoint_url + "{{{{ function.hardcoded.path }}}}".format(
        **{{{{ parameter.mapping.path|default({{}}) }}}}
    ),
    query_params={{{{ parameter.mapping.query|default({{}}) }}}},
    data={{{{ parameter.mapping.header|default({{}}) }}}}
)
"""
