import yaml


def get_password():
    variables = yaml.safe_load(open(
        'playbooks/gitlab/inventory/group_vars/gitlab.yml'))
    return variables['gitlab_password']
