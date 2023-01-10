def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,icinga-host,packages-host,website-host,deleted-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="icinga",
        help="service"
    )
