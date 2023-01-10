def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,packages-host,gitlab-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="api",
        help="service"
    )
