#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Standard Imports """
from os import environ
from os.path import exists

environ["REGSCALE_USER"] = "beaton"
environ["REGSCALE_PASSWORD"] = "&5im!TE#rPK&Zp"


def pytest_configure(config):
    """PyTest Configuration"""
    init = """
        oscal_location: /opt/OSCAL
        adAccessToken: Bearer <my token>
        adAuthUrl: https://login.microsoftonline.com/
        adClientId: <myclientidgoeshere>
        adAccessToken: Bearer <my token>
        adAuthUrl: https://login.microsoftonline.com/
        adClientId: <myclientidgoeshere>
        adGraphUrl: myUrl
        adSecret: <mysecretgoeshere>
        adTenantId: <mytenantidgoeshere>
        domain: https://dev.regscale.com
        jiraApiToken: <jiraAPIToken>
        jiraUrl: myjiraUrl
        jiraUserName: VALUE
        snowPassword: VALUE
        snowUrl: myUrl
        snowUserName: VALUE
        token: Bearer bunk_string
        userId: enter user id here
        wizAccessToken: <createdProgrammatically>
        wizAuthUrl: VALUE
        wizClientId: VALUE
        wizClientSecret: VALUE
        wizExcludes: VALUE
        wizScope: VALUE
        wizUrl: https://auth.wiz.io/oauth/token
        tenable_access_key: d51028650f9640e4a9d783cfa5156793
        tenable_secret_key: 5f27609ff91a42a5a77a880d9a989e87
        issue:
          critical: 3
          high: 5
          moderate: 30
          status: Draft
        tenable_url: https://sc.tenalab.online
    """
    file_exists = exists("init.yaml")
    if not file_exists:
        with open("init.yaml", "w", encoding="utf-8") as file:
            file.write(init)


# other config
