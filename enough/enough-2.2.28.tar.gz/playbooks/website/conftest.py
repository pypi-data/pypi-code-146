def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,website-host,proxy-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="website",
        help="service"
    )
