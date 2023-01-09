"""Git helpers
"""
import os
import re
from pathlib import Path
from pydash import py_

from eze.utils.error import EzeFileAccessError, EzeError
from eze.utils.io.file import load_text
from eze.utils.log import log_error

MAX_RECURSION: int = 10

try:
    import git
except ImportError:
    # WORKAROUND: see "ImportError: Bad git executable."
    # see https://github.com/gitpython-developers/GitPython/issues/816
    log_error("Git not installed, eze will not be able to detect git branches")


def clean_url(url: str) -> str:
    """Clean up url and remove any embedded credentials, remove trailing .git to normalise git url"""
    cleaned_url = re.sub("//[^@]+@", "//", url)
    cleaned_url = re.sub("\\.git$", "", cleaned_url)
    return cleaned_url


def sanitise_repo_url(repo_url: str) -> str:
    """
    CVE-2022-24439: sanitization of url to prevent bash script injection attacks in underlying GitPythion implementation

    warning: git clone has bug https://github.com/gitpython-developers/GitPython/issues/1515
    """
    cleaned_url = re.sub(" ", "_", repo_url)
    cleaned_url = re.sub("--", "__", cleaned_url)
    return cleaned_url


def get_active_branch(git_dir: str) -> object:
    """recursive git repo check will return branch object if found"""
    git_path = Path(git_dir)
    i = 0
    while git_path and i < MAX_RECURSION:
        branch = _get_active_branch(git_path)
        if branch:
            return branch
        git_path /= ".."
        i += 1

    return None


def _get_active_branch(git_dir: str) -> object:
    """non-recursive git repo check will return branch object if found"""
    try:
        repo = git.Repo(git_dir)
        git_branch = repo.active_branch
    except NameError:
        # INFO: git will not exist when git not installed
        git_branch = None
    except git.GitError:
        # in particular git.InvalidGitRepositoryError
        git_branch = None
    except TypeError:
        # INFO: CI often checkout as detached head which doesn't technically have a branch
        # aka throws "TypeError: HEAD is a detached symbolic reference as it points to xxxx"
        git_branch = None
    except OSError:
        git_branch = None

    return git_branch


def get_active_branch_uri(git_dir: str) -> str:
    """given dir will check repo latest uri"""
    branch = get_active_branch(git_dir)
    git_uri = py_.get(branch, "repo.remotes.origin.url", None)
    if git_uri:
        # remove any credentials inside repo url
        return clean_url(git_uri)

    ci_uri = (
        # FROM Microsoft ADO: Build.Repository.Uri = BUILD_REPOSITORY_URI
        # https://docs.microsoft.com/en-us/azure/devops/pipelines/build/variables?view=azure-devops&tabs=yaml
        os.environ.get("BUILD_REPOSITORY_URI")
        # FROM AWS Amplify: AWS_CLONE_URL
        # https://docs.aws.amazon.com/amplify/latest/userguide/environment-variables.html#amplify-console-environment-variables
        or os.environ.get("AWS_CLONE_URL")
        # FROM JENKINS toolchain: GIT_LOCAL_BRANCH & GIT_BRANCH
        # https://plugins.jenkins.io/git/#environment-variables
        # FROM IBMCLOUD toolchain: GIT_URL
        # https://github.com/ibm-cloud-docs/ContinuousDelivery/blob/master/pipeline_deploy_var.md
        or os.environ.get("GIT_URL")
        # GCP ci: _REPO_URL
        # https://cloud.google.com/build/docs/configuring-builds/substitute-variable-values
        or os.environ.get("_REPO_URL")
        # FROM Gitlab CI: CI_REPOSITORY_URL
        # https://docs.gitlab.com/ee/ci/variables/predefined_variables.html
        or os.environ.get("CI_REPOSITORY_URL")
        # FROM Github CI: GITHUB_SERVER_URL + GITHUB_REPOSITORY
        # https://docs.github.com/en/actions/reference/environment-variables
        or (
            os.environ.get("GITHUB_SERVER_URL")
            and (os.environ.get("GITHUB_SERVER_URL") + "/" + os.environ.get("GITHUB_REPOSITORY"))
        )
    )
    if not ci_uri:
        return None
    # remove any credentials inside repo url
    return clean_url(ci_uri)


def get_active_branch_name(git_dir: str) -> str:
    """given dir will check repo latest branch"""
    branch = get_active_branch(git_dir)
    git_branchname = py_.get(branch, "name", None)
    if git_branchname:
        return git_branchname

    # SPECIAL ADO PULL REQUEST LOGIC
    # when BUILD_SOURCEBRANCH starts with 'refs/heads/' normal BUILD_SOURCEBRANCHNAME
    # when BUILD_SOURCEBRANCH starts with 'refs/pull/' pr, SYSTEM_PULLREQUEST_SOURCEBRANCH contains merge
    # https://docs.microsoft.com/en-us/azure/devops/pipelines/build/variables?view=azure-devops&tabs=yaml
    ado_source_branch = os.environ.get("BUILD_SOURCEBRANCH")
    if ado_source_branch and ado_source_branch.startswith("refs/pull/"):
        return os.environ.get("SYSTEM_PULLREQUEST_SOURCEBRANCH").replace("refs/heads/", "")

    ci_branchname = (
        # FROM ADO: Standard ADO non PR case, BUILD_SOURCEBRANCHNAME
        # https://docs.microsoft.com/en-us/azure/devops/pipelines/build/variables?view=azure-devops&tabs=yaml
        os.environ.get("BUILD_SOURCEBRANCHNAME")
        # FROM AWS Amplify: AWS_BRANCH
        # https://docs.aws.amazon.com/amplify/latest/userguide/environment-variables.html#amplify-console-environment-variables
        or os.environ.get("AWS_BRANCH")
        # FROM JENKINS toolchain: GIT_LOCAL_BRANCH & GIT_BRANCH
        # https://plugins.jenkins.io/git/#environment-variables
        # FROM IBMCLOUD toolchain: GIT_BRANCH
        # https://github.com/ibm-cloud-docs/ContinuousDelivery/blob/master/pipeline_deploy_var.md
        or os.environ.get("GIT_LOCAL_BRANCH")
        or os.environ.get("GIT_BRANCH")
        # FROM GCP ci: BRANCH_NAME
        # https://cloud.google.com/build/docs/configuring-builds/substitute-variable-values
        or os.environ.get("BRANCH_NAME")
        #  Gitlab CI: CI_COMMIT_BRANCH & CI_DEFAULT_BRANCH
        # https://docs.gitlab.com/ee/ci/variables/predefined_variables.html
        or os.environ.get("CI_COMMIT_BRANCH")
        or os.environ.get("CI_MERGE_REQUEST_TARGET_BRANCH_NAME")
        or os.environ.get("CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_NAME")
        or os.environ.get("CI_DEFAULT_BRANCH")
        # FROM Github CI: GITHUB_REF
        # https://docs.github.com/en/actions/reference/environment-variables
        or os.environ.get("GITHUB_REF")
    )
    if ci_branchname:
        return ci_branchname

    return None


def get_gitignore_paths(git_dir: str = None) -> list:
    """will retrieve list of gitignore paths"""
    if git_dir:
        git_path = Path(git_dir)
    else:
        git_path = Path.cwd()
    gitignore = git_path / ".gitignore"
    try:
        gitignore_txt = load_text(gitignore)
    except EzeFileAccessError:
        return []
    gitignore_lines: list = [
        x for x in gitignore_txt.split("\n") if not x.strip().startswith("#") and not x.strip() == ""
    ]
    return gitignore_lines


def get_gitignore_regexes(git_dir: str = None, *, extra_paths: list = None) -> tuple:
    """will retrieve list of gitignore paths as regex"""
    gitignore_paths: list = get_gitignore_paths(git_dir)
    if extra_paths:
        gitignore_paths.append(extra_paths)
    force_includes: list = []
    excludes: list = []
    for gitignore_path in gitignore_paths:
        if gitignore_path[0] == "!":
            force_includes.append(re.sub("^!", "", gitignore_path))
        else:
            excludes.append(gitignore_path)

    return (_convert_gitignores_to_regex(force_includes), _convert_gitignores_to_regex(excludes))


def get_compiled_gitignore_regexes(git_dir: str = None, *, extra_paths: list = None) -> tuple:
    """will retrieve list of gitignore paths as regex"""
    (force_includes, excludes) = get_gitignore_regexes(git_dir, extra_paths=extra_paths)

    return ([safe_compile(regex) for regex in force_includes], [safe_compile(regex) for regex in excludes])


def safe_compile(regex: str):
    try:
        return re.compile(regex)
    except Exception as error:
        return re.compile("^__BROKEN_REGEX__$")


def is_file_gitignored(filepath: str, compiled_gitignore_regexes: tuple) -> list:
    """will retrieve list of gitignore paths as regex"""
    (force_includes, excludes) = compiled_gitignore_regexes
    for regex in force_includes:
        if regex.match(filepath):
            return False
    for regex in excludes:
        if regex.match(filepath):
            return True
    return False


def _convert_gitignores_to_regex(gitignore_paths: list) -> list:
    """quick in dirty"""
    gitignore_paths = [re.sub("([.+$()|/])", "[\\1]", str(line)) for line in gitignore_paths]
    gitignore_paths = [re.sub("(\\^)", "\\\\^", line) for line in gitignore_paths]
    gitignore_paths = [re.sub("(\\\\\\?)", "__WILDCARD__", line) for line in gitignore_paths]
    gitignore_paths = [re.sub("[?]", "[^/]", line) for line in gitignore_paths]
    gitignore_paths = [re.sub("__WILDCARD__", "\\\\?", line) for line in gitignore_paths]
    gitignore_paths = [re.sub("\\*\\*", "__WILDCARD__", line) for line in gitignore_paths]
    gitignore_paths = [re.sub("\\*", "[^/]*", line) for line in gitignore_paths]
    gitignore_paths = [re.sub("__WILDCARD__", ".*", line) for line in gitignore_paths]
    gitignore_paths = ["^" + line for line in gitignore_paths]
    return gitignore_paths


def clone_repo(clone_dir: str, repo_url: str, branch: str):
    """
    clone repo using git clone command

    warning: git clone has bug https://github.com/gitpython-developers/GitPython/issues/1515

    CVE-2022-24439: sanitization applied to url to prevent exploitation
    """
    try:
        os.chdir(clone_dir)
        # #86: santisating urls to prevent exceptions
        sanitised_repo_url = sanitise_repo_url(repo_url)
        repo = git.Repo.clone_from(sanitised_repo_url, clone_dir, branch=branch)
    except git.exc.GitCommandError as error:
        raise EzeError(f"""on cloning remote branch '{branch}' process, {error.stderr}""")
    os.chdir(clone_dir)
