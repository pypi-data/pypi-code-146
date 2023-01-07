# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['msal_streamlit_authentication']

package_data = \
{'': ['*'],
 'msal_streamlit_authentication': ['frontend/dist/*', 'frontend/dist/assets/*']}

install_requires = \
['streamlit']

setup_kwargs = {
    'name': 'msal-streamlit-authentication',
    'version': '1.0.6',
    'description': 'Streamlit Authentication library based on MSAL.JS',
    'long_description': '# OpenID Connect (OIDC) authentication component for Streamlit\n\n## About\n\nThis Streamlit component enables client-side authentication using [Azure AD](https://docs.microsoft.com/azure/active-directory/develop/v2-overview) work and school accounts (AAD), Microsoft personal accounts (MSA) and social identity providers like Facebook, Google, LinkedIn, Microsoft accounts, etc. through [Azure AD B2C](https://docs.microsoft.com/azure/active-directory-b2c/active-directory-b2c-overview#identity-providers) service.\nThe component is achieving this by applying the [Microsoft MSAL JS Library](https://github.com/AzureAD/microsoft-authentication-library-for-js/tree/dev/lib/msal-browser) inside of a React project. Since the component is based on MSAL, it can be configured to support any provider that supports the OpenID Connect Authorization Code Flow (PKCE).\nFor more information on MSAL, consult the [Github project](https://github.com/AzureAD/microsoft-authentication-library-for-js/tree/dev/lib/msal-browser) and its [offical documentation](https://learn.microsoft.com/en-us/azure/active-directory/develop/msal-overview).\n\n## Usage\n\nBelow is a sample Python snippet displaying how to apply component. Visually, the component gives rise to a single button\nin the Streamlit Dashboard with a text that depends on whether an active login session exists. The `auth` and `cache`\nparameters are entirely equivalent to the properties mentioned in the [Github documentation](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/initialization.md).\nThe `login_request` and `logout_request` parameters are covered [here](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/login-user.md).\n```python\nimport streamlit as st\nfrom msal_streamlit_authentication import msal_authentication\n\n\nlogin_token = msal_authentication(\n    auth={\n        "clientId": "aaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee",\n        "authority": "https://login.microsoftonline.com/aaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee",\n        "redirectUri": "/",\n        "postLogoutRedirectUri": "/"\n    }, # Corresponds to the \'auth\' configuration for an MSAL Instance\n    cache={\n        "cacheLocation": "sessionStorage",\n        "storeAuthStateInCookie": False\n    }, # Corresponds to the \'cache\' configuration for an MSAL Instance\n    login_request={\n        "scopes": ["aaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee/.default"]\n    }, # Optional\n    logout_request={}, # Optional\n    login_button_text="Login", # Optional, defaults to "Login"\n    logout_button_text="Logout", # Optional, defaults to "Logout"\n    key=1 # Optional if only a single instance is needed\n)\nst.write("Recevied login token:", login_token)\n```\nThe component currently expects for the user to go through a popup based login flow.\nFurther flows may be supported at a later time. As discussed [here](https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/initialization.md#optional-configure-authority),\nthe `protocolMode` parameter in `auth` can be used to configure OIDC providers that differ from Azure AD.\n\n## Inspiration\nInspired by [official Streamlit template](https://github.com/streamlit/component-template), [this tutorial](https://youtu.be/htXgwEXwmNs) ([Github](https://github.com/andfanilo/streamlit-plotly-component-tutorial)) and the official [Streamlit NPM component-lib](https://github.com/streamlit/streamlit/tree/develop/component-lib).\n\n',
    'author': 'Michael Staal-Olsen',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mstaal/msal_streamlit_authentication',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.12,<3.12',
}


setup(**setup_kwargs)
