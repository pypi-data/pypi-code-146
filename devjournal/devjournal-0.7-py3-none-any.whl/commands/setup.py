from rich.prompt import Prompt

from devjournal.config import Config


def setup():
    if url := Prompt.ask(
        "URL of remote repo (example: git@github.com:Godsmith/devjournal-entries.git)",
        default="",
        show_default=True,
    ):
        branch = Prompt.ask(
            "Name of remote branch (must have at least one commit)",
            default="main",
            show_default=True,
        )
        # TODO: check if config valid here
        config = Config(remote_repo_url=url, remote_branch=branch)
        config.write()
        print(f"Config saved to {config.path}.")
