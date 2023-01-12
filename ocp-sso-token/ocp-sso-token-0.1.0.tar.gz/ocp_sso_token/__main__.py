"""Obtain an OCP OAuth token for an SSO IdP with Kerberos support."""

import argparse
import typing

from . import ocp_oauth_login


def main(argv: typing.Optional[typing.List[str]] = None) -> None:
    """Obtain an OCP OAuth token for an SSO IdP with Kerberos support."""
    parser = argparse.ArgumentParser(description='Obtain an OCP OAuth token for a Kerberos ticket',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('api_url', help='Cluster API URL like https://api.cluster:6443')
    parser.add_argument('--identity-providers', default='SSO,OpenID',
                        help='Identity provider names')
    args = parser.parse_args(argv)
    login = ocp_oauth_login.OcpOAuthLogin(args.api_url)
    if not (identity_provider := next((n for n in login.identity_providers
                                       if n in args.identity_providers.split(',')), None)):
        raise Exception(f'Unable to find OpenID provider: {", ".join(login.identity_providers)}')
    print(login.token(identity_provider))


if __name__ == '__main__':
    main()
