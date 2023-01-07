import pytest
import yaml


@pytest.fixture
def domain(pytestconfig):
    inventory = pytestconfig.getoption("--ansible-inventory")
    vars_dir = f'{inventory}/group_vars/all'
    return yaml.safe_load(open(vars_dir + '/domain.yml'))['domain']


@pytest.fixture
def gitea_hostname(domain):
    return f'gitea.{domain}'


@pytest.fixture
def woodpecker_hostname(domain):
    return f'woodpecker.{domain}'


@pytest.fixture
def certs(request):
    return request.session.infrastructure.certs()


@pytest.fixture
def root_password():
    # must match playbooks/hostea/inventory/host_vars/gitea-host/gitea.yml
    return "etquofEtseudett"


@pytest.fixture
def make_user(root_password):

    contexts = []

    def _make_user(forge, username, password):
        forge.authenticate(username="root", password=root_password)
        user = forge.users.get(username)
        if user:
            for project in user.projects:
                forge.projects.delete(username, project.project)

            forge.users.delete(username)
        email = f"{username}@example.com"
        user = forge.users.create(username, password, email)
        contexts.append((forge, username))
        return user

    yield _make_user

    for (forge, username) in contexts:
        if not forge.is_authenticated or not forge.is_admin:
            forge.authenticate(username="root", password=root_password)
        user = forge.users.get(username)
        if user:
            for project in user.projects:
                forge.projects.delete(username, project.project)
        forge.users.delete(username)


@pytest.fixture
def make_project(root_password):

    contexts = []

    def _make_project(forge, username, project, **data):
        forge.projects.delete(username, project)
        p = forge.projects.create(username, project, **data)
        contexts.append((forge, username, project))
        return p

    yield _make_project

    for (forge, username, project) in contexts:
        forge.authenticate(username="root", password=root_password)
        forge.projects.delete(username, project)
