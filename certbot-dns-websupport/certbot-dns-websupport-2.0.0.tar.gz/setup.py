# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['certbot_dns_websupport', 'certbot_dns_websupport._internal']

package_data = \
{'': ['*']}

install_requires = \
['certbot>=2.0.0,<3.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'certbot.plugins': ['dns-websupport = '
                     'certbot_dns_websupport._internal.dns_websupport:Authenticator']}

setup_kwargs = {
    'name': 'certbot-dns-websupport',
    'version': '2.0.0',
    'description': 'This is a plugin for Certbot that uses the Websupport REST API to allow Websupport customers to prove control of a domain name.',
    'long_description': '# certbot-dns-websupport\n\n[Websupport.sk](https://www.websupport.sk) DNS Authenticator plugin for Certbot\n\nThis plugin automates the process of completing a `dns-01` challenge by\ncreating, and subsequently removing, TXT records using the Websupport Remote API.\n\n---\n\n## Installation\n\n```bash\npip install certbot-dns-websupport\n```\n\n---\n\n## Named Arguments\n\nTo start using DNS authentication for Websupport, pass the following arguments on\ncertbot\'s command line:\n\n| Command                                                   | Description                                                                                                  |\n| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |\n| `--authenticator dns-websupport`                          | select the authenticator plugin (Required)                                                                   |\n| `--dns-websupport-credentials "/path/to/credentials.ini"` | websupport user INI file. (Required)                                                                         |\n| `--dns-websupport-propagation-seconds "120"`              | waiting time for DNS to propagate before the ACMEserver to verify the DNS (Default: 60, Recommended: >= 120) |\n\n---\n\n## Credentials file\n\nObtain an identifier and secret key (see [Account Page](https://admin.websupport.sk/sk/auth/apiKey))\n\nAn example `credentials.ini` file:\n\n```ini\ndns_websupport_identifier = <identifier>\ndns_websupport_secret_key = <secret_key>\n```\n\nThe path to this file can be provided interactively or using the\n`--dns-websupport-credentials` command-line argument. Certbot\nrecords the path to this file for use during renewal, but does not store the\nfile\'s contents.\n\n**CAUTION:** You should protect these API credentials as you would the\npassword to your websupport account. Users who can read this file can use these\ncredentials to issue arbitrary API calls on your behalf. Users who can cause\nCertbot to run using these credentials can complete a `dns-01` challenge to\nacquire new certificates or revoke existing certificates for associated\ndomains, even if those domains aren\'t being managed by this server.\n\nCertbot will emit a warning if it detects that the credentials file can be\naccessed by other users on your system. The warning reads "Unsafe permissions\non credentials configuration file", followed by the path to the credentials\nfile. This warning will be emitted each time Certbot uses the credentials file,\nincluding for renewal, and cannot be silenced except by addressing the issue\n(e.g., by using a command like `chmod 600` to restrict access to the file).\n\n<br>\n\n**It is suggested to secure the .ini folder as follows:**\n\n```commandline\nchown root:root /etc/letsencrypt/.secrets\nchmod 600 /etc/letsencrypt/.secrets\n```\n\n---\n\n## Direct command\n\nTo acquire a single certificate for `*.example.com`, waiting 600 seconds for DNS propagation:\n\n```commandline\ncertbot certonly \\\n    --authenticator dns-websupport \\\n    --dns-websupport-propagation-seconds "600" \\\n    --dns-websupport-credentials "/etc/letsencrypt/.secrets/credentials.ini" \\\n    --email full.name@example.com \\\n    --agree-tos \\\n    --non-interactive \\\n    --rsa-key-size 4096 \\\n    -d *.example.com\n```\n\n**NOTE:** Don\'t forget to properly edit your ini file name and mail address.\n\n---\n\n## Auto renew\n\nAdd cronjob:\n\n```commandline\n0 3 * * * certbot renew \\\n    --authenticator dns-websupport \\\n    --dns-websupport-propagation-seconds "600" \\\n    --dns-websupport-credentials "/etc/letsencrypt/.secrets/credentials.ini" \\\n    --post-hook "systemctl reload nginx"\n```\n\n## Docker\n\nIn order to create a docker container with a certbot-dns-websupport installation,\ncreate an empty directory with the following `Dockerfile`:\n\n```dockerfile\nFROM certbot/certbot\nRUN pip3 install certbot-dns-websupport\n```\n\n<br>\n\nProceed to build the image:\n\n```commandline\ndocker build -t certbot/dns-websupport .\n```\n\n<br>\n\nOnce that\'s finished, the application can be run as follows:\n\n```commandline\nsudo docker run -it --rm \\\n    -v /var/lib/letsencrypt:/var/lib/letsencrypt \\\n    -v /etc/letsencrypt:/etc/letsencrypt \\\n    certbot/dns-websupport \\\n    certonly \\\n    --authenticator dns-websupport \\\n    --dns-websupport-propagation-seconds "600" \\\n    --dns-websupport-credentials "/etc/letsencrypt/.secrets/credentials.ini" \\\n    --email full.name@example.com \\\n    --agree-tos \\\n    --non-interactive \\\n    --rsa-key-size 4096 \\\n    -d *.example.com\n```\n\n**NOTE:** Check if your volumes on host system match this example (Depends if you installed your server on host system or inside docker). If not, you will have to edit this command. Also don\'t forget to properly edit your ini file name and mail address.\n\n---\n',
    'author': 'johnybx',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/johnybx/certbot-dns-websupport',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
