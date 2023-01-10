import re
import subprocess as sp
from shutil import which, copy2

from termcolor import colored

VERSION_TARGET = '1.12.141'


def setup(certs_path=None, version=VERSION_TARGET, verbosity='m') -> None:
    """Set up the python provider infrastructure.

    This will do the following:
        * install the dotnet tool.
        * copy the certs at a given path to the tool's directory.

    Args:
        certs_path (str): path to your .pem files
        version (Optional[str]): optional version specification. Defaults to 1.11.25.
        verbosity (str): verbosity of the dotnet install process. Allowed values are q[uiet], m[inimal], n[ormal],
        d[etailed], and diag[nostic]. Defaults to 'm'

    """

    if re.match('^[0-9.]*$', version) is None:
        raise ValueError(f'The input to version was not a valid semver: {version}')
    if verbosity not in ['q', 'm', 'n', 'd', 'diag']:
        raise ValueError(
            f'The input to verbosity was invalid: {verbosity}. '
            f'Allowed values are q[uiet], m[inimal], n[ormal], d[etailed], and diag[nostic]. Defaults to "m"'
        )

    print("Setting up the required parts for python providers 🛠")

    action = 'install' if which('luminesce-python-providers') is None else 'update'
    print(f"  • {action} dotnet tool ({version})")

    cmd = f'dotnet tool {action} -g finbourne.luminesce.pythonproviders '
    cmd += f'--verbosity={verbosity}  --version={version} --no-cache '

    p = sp.Popen(cmd.split(), stdout=sp.PIPE, bufsize=1, universal_newlines=True)
    indent = ' ' * 6
    with p:
        for i, line in enumerate(p.stdout):
            if i == 0:
                line = line.lstrip()
            print(colored(f'{indent}{line}', 'green'), end='')

    if certs_path is not None:
        print(f"  • copy certs from {certs_path}")
        copy_certs(certs_path, version)

    print("All set! You can now build and run python Luminesce providers.")


def copy_certs(certs_path, version=VERSION_TARGET):
    loc = which('luminesce-python-providers')
    if loc is None:
        raise ValueError(
            'Could not find luminesce-python-providers - installation may have failed, or dotnet tools are not on $PATH'
        )

    path = '/'.join(loc.split('/')[:-1])
    path += f'/.store/finbourne.luminesce.pythonproviders/{version}/'
    path += f'finbourne.luminesce.pythonproviders/{version}/tools/net6.0/any/'

    copy2(certs_path + '/client_cert.pem', path)
    copy2(certs_path + '/client_key.pem', path)


def run_test_provider(domain='fbn-prd'):
    """Builds and starts a test provider to make sure everything works. The name of the provider will be
    Pandas.TestProvider.
    You should see a login window pop up. Sign in and you should be good to do.

    Args:
        domain (Optional[str]): the domain to run in. Defaults to fbn-prd.

    """

    import pandas as pd
    import numpy as np
    from .implementation.pandas_provider import PandasProvider
    from .manager import ProviderManager

    df = pd.DataFrame({f'Col{i}': np.random.uniform(-1, 1, size=100) for i in range(10)})
    p = PandasProvider(df, 'TestProvider')
    ProviderManager(p, domain=domain).run()
