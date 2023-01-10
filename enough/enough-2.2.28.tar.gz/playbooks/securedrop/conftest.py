def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,securedrop-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="securedrop",
        help="service"
    )
