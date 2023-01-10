import argparse
from importlib.util import find_spec

import lumipy.provider as lp
from lumipy.provider.setup import VERSION_TARGET
from lumipy.test.provider.int_test_providers import (
    ParameterAndLimitTestProvider,
    IntSerialisationBugProvider,
    TableParameterTestProvider,
    PandasFilteringTestProvider,
    FilteringTestProvider,
    ColumnValidationTestProvider,
    TaskCancelledTestProvider,
    TestLogAndErrorLines,
    NothingProvider,
    UnicodeProvider,
)

_provider_sets = {
    'test': [
        ParameterAndLimitTestProvider(),
        IntSerialisationBugProvider(),
        TableParameterTestProvider(),
        PandasFilteringTestProvider(1989),
        FilteringTestProvider(),
        ColumnValidationTestProvider(),
        TaskCancelledTestProvider(),
        TestLogAndErrorLines(),
        NothingProvider(),
        UnicodeProvider(1989),
    ],
}
if find_spec('cvxopt') is not None and find_spec('yfinance') is not None:
    _provider_sets['portfolio_opt'] = [lp.YFinanceProvider(), lp.QuadraticProgram()]


def get_providers(provider_set):

    if provider_set in _provider_sets.keys():
        return _provider_sets[provider_set]
    else:
        set_names = ', '.join(sorted(_provider_sets.keys()))
        raise ValueError(f'Unrecognised provider set: "{provider_set}".\nSupported values are {set_names}')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'action',
        choices=['setup', 'run'],
        help='The lumipy.providers action to run. Available actions are: [setup] sets up the python providers. '
             'This will install/update the dotnet tool and (optionally) copy your certs to the tool\'s directory.'
    )
    parser.add_argument(
        '--certs_path',
        dest='certs_path',
        default=None,
        help='The path to your luminesce .pem files. Optional, but you\'ll need to use lumipy.provider.copy_certs '
             'later before you run anything.'
    )
    parser.add_argument(
        '--version',
        dest='version',
        default=VERSION_TARGET,
        help=f'The version of the dotnet tool to install. Optional, defaults to {VERSION_TARGET}'
    )
    parser.add_argument(
        '--verbosity',
        dest='verbosity',
        default='m',
        help='verbosity of the dotnet install process. Allowed values are q[uiet], m[inimal], n[ormal], d[etailed], '
             'and diag[nostic]. Defaults to "m".'
    )
    parser.add_argument(
        '--set',
        dest='provider_set',
        default=None,
        help='Which set of providers to run'
    )
    parser.add_argument(
        '--user',
        dest='user',
        default=None,
        help='Routing for the providers. Can be a user ID, global, or i not specified will open a browser window for '
             'you to login.'
    )
    parser.add_argument(
        '--domain',
        dest='domain',
        default=None,
        help='Domain to run the provider in.'
    )
    parser.add_argument(
        '--port',
        dest='port',
        default=5001,
        help='The port to run the python providers\' api server at',
        type=int
    )
    parser.add_argument(
        '--fbn-run',
        dest='fbn_run',
        action='store_true',
        help='Whether to use the fbn k8s authentication when running on the FINBOURNE estate. '
    )
    parser.add_argument(
        '--dry-run',
        dest='dry_run',
        action='store_true',
        help='Whether to run just the python API for testing, and not to connect to luminesce.'
    )
    args = parser.parse_args()

    if args.action == 'setup':
        lp.setup(args.certs_path, args.version, args.verbosity)

    if args.action == 'run':
        providers = get_providers(args.provider_set)
        lp.ProviderManager(*providers, user=args.user, domain=args.domain, port=args.port, dry_run=args.dry_run, _fbn_run=args.fbn_run).run()
