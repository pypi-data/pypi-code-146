import click
from pprint import pprint
from json import dumps


@click.group()
def github_cli():
    pass


@click.command('get-commits-sha-from-merge-commit')
@click.option('--owner', help='GitHub owner name', default='gisce', show_default=True)
@click.option('--repository', help='GitHub repository name', default='erp', show_default=True)
@click.option("--sha", help="Merge commit sha", required=True, type=click.STRING)
def get_commits_sha_from_merge_commit(owner, repository, sha):
    from giscemultitools.githubutils.utils import GithubUtils
    res = GithubUtils.get_commits_sha_from_merge_commit(owner=owner, repository=repository, sha=sha)
    print(dumps(res))


@click.command('get-pullrequest-info')
@click.option('--owner', help='GitHub owner name', default='gisce', show_default=True)
@click.option('--repository', help='GitHub repository name', default='erp', show_default=True)
@click.option("--pr", help="PR number", required=True, type=click.STRING)
def get_pullrequest_info(owner, repository, pr):
    from giscemultitools.githubutils.utils import GithubUtils
    res = GithubUtils.get_pullrequest_info(owner=owner, repository=repository, pr_number=pr)
    print(dumps(res))


@click.command('update-projectv2-card-from-id')
@click.option('--owner', help='GitHub owner name', default='gisce', show_default=True)
@click.option('--repository', help='GitHub repository name', default='erp', show_default=True)
@click.option("--project-id", help="Project ID", required=True, type=click.STRING)
@click.option("--item-id", help="Item ID", required=True, type=click.STRING)
@click.option("--field-id", help="Field ID", required=True, type=click.STRING)
@click.option("--value", help="Text value", required=True, type=click.STRING)
def update_projectv2_card_from_id(owner, repository, project_id, item_id, field_id, value):
    from giscemultitools.githubutils.utils import GithubUtils
    res = GithubUtils.update_projectv2_item_field_value(owner, repository, project_id, item_id, field_id, value)
    print(dumps(res))


github_cli.add_command(get_commits_sha_from_merge_commit)
github_cli.add_command(update_projectv2_card_from_id)
github_cli.add_command(get_pullrequest_info)


if __name__ == "__main__":
    github_cli()
