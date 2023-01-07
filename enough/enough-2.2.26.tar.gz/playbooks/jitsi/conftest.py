def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,jitsi-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="jitsi",
        help="service"
    )
