def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",
        default="bind-host,otherbind-host,bind-client-host,external-host,icinga-host,deleted-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="bind",
        help="service"
    )
