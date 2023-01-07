#
# Running hostea tests require the following to be created manually:
#
# playbooks/hostea/inventory/host_vars/bind-host/enough-api-token.yml
# enough_api_token: xxxxxx
#
# playbooks/hostea/templates/clouds.yml using
#   playbooks/hostea/templates/clouds.yml.sample as an example
#
#
def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,gitea-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="hostea",
        help="service"
    )
