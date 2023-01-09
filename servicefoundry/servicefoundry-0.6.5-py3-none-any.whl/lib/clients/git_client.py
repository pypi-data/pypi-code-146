from __future__ import annotations

import os

import git
from pydantic import BaseModel

from servicefoundry.logger import logger


class GitRepo(BaseModel):
    # The git repository URL
    repo_url: str
    # Can be branch or git tag
    git_ref: str
    # Git username
    username: str
    # Git password
    password: str


class GitClient:
    def __init__(self) -> None:
        # TODO: Don't think this will be cross platform
        self.client = git.Git(os.path.join(os.path.expanduser("~"), "git", "GitPython"))

    def execute_git_command(self, args):
        try:
            result = self.client.execute(["git", *args])
            logger.info(result)
            return result
        except Exception as e:
            raise Exception("Git command failed") from e

    # Clone the repo and return the path
    def clone_repo(self, git_repo: GitRepo, destination_dir):
        input_repo_url: str = git_repo.repo_url
        if input_repo_url.startswith("http://"):
            raise Exception("Please provide a https git repository")
        if input_repo_url.startswith("https://"):
            input_repo_url = input_repo_url[8:]
        print("Git clone link: " + f"https://{git_repo.username}@{input_repo_url}")
        if git_repo.username and git_repo.password:
            self.execute_git_command(
                [
                    "clone",
                    f"https://{git_repo.username}:{git_repo.password}@{input_repo_url}",
                    destination_dir,
                ]
            )
        else:
            self.execute_git_command(
                [
                    "clone",
                    f"{git_repo.repo_url}",
                    destination_dir,
                ]
            )

    def commit_all_changes(self, git_repo_dir, branch):
        if branch == None:
            branch = "main"

        current_dir = os.getcwd()
        os.chdir(git_repo_dir)
        # Switch to the input branch
        self.execute_git_command(["checkout", "-B", branch])

        # Add all local files
        self.execute_git_command(["add", "."])
        diff_check = self.execute_git_command(["diff", "--staged"])
        if not diff_check:
            print(f"Nothing to commit in target repo: {git_repo_dir}")
        else:
            self.execute_git_command(
                ["commit", "-m", "K8s Cluster Configuration via ArgoCD applications"]
            )
            self.execute_git_command(["push", "-f", "origin", branch])

        os.chdir(current_dir)
