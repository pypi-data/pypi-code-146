"""Provides a custom loader to load the appropriate CI provider specific environment variables"""
from os import environ

ci_loader_conf = {
    "bitbucket": {
        # REF https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/
        "commit": "BITBUCKET_COMMIT",
        "branch": "BITBUCKET_BRANCH",
        "pipeline_id": "BITBUCKET_PIPELINE_UUID",
        "job_url": {
            "format": "{0:s}/addon/pipelines/home#!/results/{1:s}/steps/{2:s}",
            "variables": [
                "BITBUCKET_GIT_HTTP_ORIGIN",
                "BITBUCKET_BUILD_NUMBER",
                "BITBUCKET_STEP_UUID",
            ],
        },
        "tag": "BITBUCKET_TAG",
    },
    "github": {
        # REF https://docs.github.com/en/actions/learn-github-actions/environment-variables
        "commit": "GITHUB_SHA",
        "branch": "GITHUB_REF_NAME",
        "pipeline_id": "GITHUB_RUN_ID",
        "job_url": {
            "format": "{0:s}/{1:s}/actions/runs/{2!s:s}",
            "variables": [
                "GITHUB_SERVER_URL",
                "GITHUB_REPOSITORY",
                "GITHUB_RUN_ID",
            ],
        },
        "tag": "GITHUB_REF_NAME",
    },
    "gitlab": {
        # REF https://docs.gitlab.com/ee/ci/variables/predefined_variables.html
        "commit": "CI_COMMIT_SHA",
        "branch": "CI_COMMIT_REF_NAME",
        "pipeline_id": "CI_PIPELINE_ID",
        "job_url": {
            "format": "{0:s}",
            "variables": [
                "CI_JOB_URL",
            ],
        },
        "tag": "CI_COMMIT_TAG",
    },
    "azure": {
        "commit": "BUILD_SOURCEVERSION",
        "branch": "BUILD_SOURCEBRANCHNAME",
        "pipeline_id": "SYSTEM_TIMELINEID",
        "job_url": {
            "format": "{0:s}{1:s}/_build/results?buildId={2:s}&view=logs&j={3:s}&t={4:s}",
            "variables": [
                "SYSTEM_COLLECTIONURI",
                "SYSTEM_TEAMPROJECT",
                "BUILD_BUILDID",
                "SYSTEM_JOBID",
                "SYSTEM_TASKINSTANCEID",
            ],
        },
    },
}
# this is a required function signature so there are going to be unused arguments
# pylint: disable=unused-argument
def load(obj, env=None, silent=True, key=None, filename=None):
    """
    Reads and loads in to "obj" a single key or all keys from source
    :param obj: the settings instance
    :param env: settings current env (upper case) default='DEVELOPMENT'
    :param silent: if errors should raise
    :param key: if defined load a single key, else load all from `env`
    :param filename: Custom filename to load (useful for tests)
    :return: None
    """
    # Load data from your custom data source (file, database, memory etc)
    # use `obj.set(key, value)` or `obj.update(dict)` to load data
    # use `obj.find_file('filename.ext')` to find the file in search tree
    # Return nothing

    ci_config_dict = {"provider": "LOCAL"}
    for ci_provider, ci_provider_env_cfg in ci_loader_conf.items():
        if not ci_provider_env_cfg["commit"] in environ:
            continue

        ci_config_dict["provider"] = ci_provider
        ci_config_dict["commit"] = environ.get(ci_provider_env_cfg["commit"])
        ci_config_dict["branch"] = environ.get(ci_provider_env_cfg["branch"])
        ci_config_dict["pipeline_id"] = environ.get(ci_provider_env_cfg["pipeline_id"])
        ci_config_dict["tag"] = environ.get(ci_provider_env_cfg["tag"])

        job_url_cnf = ci_provider_env_cfg["job_url"]
        ci_config_dict["job_url"] = job_url_cnf["format"].format(
            *[environ[env_var] for env_var in job_url_cnf["variables"]]
        )
        break
    obj.update(ci_config_dict)
