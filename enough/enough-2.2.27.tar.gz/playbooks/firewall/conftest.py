def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="server-host,client-host,external-host,gitlab-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="firewall",
        help="service"
    )
