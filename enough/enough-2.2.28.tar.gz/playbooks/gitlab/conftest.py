def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,runner-host,postfix-host,gitlab-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="gitlab",
        help="service"
    )
