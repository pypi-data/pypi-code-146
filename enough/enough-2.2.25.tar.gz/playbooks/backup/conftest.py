def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,packages-host,pet-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="backup",
        help="service"
    )
