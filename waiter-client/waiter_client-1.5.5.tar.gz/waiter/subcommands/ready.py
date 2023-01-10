
from waiter.action import check_ssl, process_ping_request
from waiter.util import check_positive, guard_no_cluster


def ready(clusters, args, _, __):
    """Ensure the Waiter service is ready for traffic."""
    guard_no_cluster(clusters)
    token_name = args.get('token')
    timeout_secs = args.get('timeout', None)
    if not process_ping_request(clusters, token_name, False, timeout_secs, True):
        return 1
    ssl_success = check_ssl(token_name, timeout_secs)
    return 0 if ssl_success else 1


def register(add_parser):
    """Adds this sub-command's parser and returns the action function"""
    default_timeout = 300
    parser = add_parser('ready', help='ensure the target token is ready for traffic')
    parser.add_argument('token')
    parser.add_argument('--timeout', '-t', help=f'read timeout (in seconds) for requests (default is '
                                                f'{default_timeout} seconds)',
                        type=check_positive, default=default_timeout)
    return ready

