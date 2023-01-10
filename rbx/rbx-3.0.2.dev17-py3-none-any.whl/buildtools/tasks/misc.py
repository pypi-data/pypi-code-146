from os import path

import invoke
from six import PY2


def run(ctx, command):
    result = ctx.run(command, hide="out").stdout
    if PY2:
        result = result.decode("utf-8")
    return result.rstrip()


@invoke.task(name="git-next-tag")
def get_next_tag(ctx):
    """A helper to generate the next tag based on the current git tag.

    To use in Jenkins job:

        >>> export VERSION=`invoke misc.git-next-tag`

    Expects an integer, otherwise will start at 1.
    """
    tag = run(ctx, "git describe --tags $(git rev-list --tags --max-count=1)")
    try:
        tag = int(tag)
    except ValueError:
        tag = 0
    print(tag + 1)


@invoke.task(name="git-merge-desc")
def get_merge_desc(ctx):
    """A helper to get the description of a merge commit.

    To use in a Jenkins job:

        >>> export DESCRIPTION=`invoke misc.git-merge-desc`

    When merging a PR the subject line will be added to the body of the merge
    commit.
    """
    print(run(ctx, 'git log -1 --pretty=format:"%b"'))


@invoke.task(name="npm-version")
def get_npm_version(ctx):
    """A helper to get the npm package version from a package.json file.

    To use in Jenkins job:

        >>> export VERSION=`invoke misc.npm-version`

    """
    if path.exists("package.json"):
        print(run(ctx, "cat package.json | jq .version -r"))
    else:
        print("unknown")
