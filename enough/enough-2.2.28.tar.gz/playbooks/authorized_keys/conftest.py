def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",
        default="authorized-keys-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="authorized_keys",
        help="service"
    )
