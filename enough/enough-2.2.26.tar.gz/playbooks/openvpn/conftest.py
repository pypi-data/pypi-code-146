def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,icinga-host,website-host,internal-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="openvpn",
        help="service"
    )
