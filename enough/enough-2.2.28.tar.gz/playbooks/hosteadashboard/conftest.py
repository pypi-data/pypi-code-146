def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,forgejo-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="hosteadashboard",
        help="service"
    )
