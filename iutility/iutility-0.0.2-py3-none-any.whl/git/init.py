import getpass
import os
import typing
from pathlib import Path

import click
import tomlkit
import tomlkit.items
from toml_sort.tomlsort import TomlSort

from ..utils import download, execute, move, remove
from .secret import cmd as cmd_secret
from .typed import GITIGNORE_API, TEMPLATE_BRANCHES, TEMPLATE_FILES, TEMPLATE_GIT


def to_pip_name(name: str) -> str:
    return name.lower().replace("-", "_")


def init_readme(name: str, description: typing.Optional[str] = None) -> None:
    with open(file="README.md", mode="w") as fp:
        lines: list[str] = [f"# {name}"]
        if description:
            lines.append("")
            lines.append(description)
        fp.writelines(lines)


def init_gitignore(gitignore: tuple[str]) -> None:
    if gitignore:
        download(
            url=GITIGNORE_API + ",".join(sorted(gitignore)),
            output=".gitignore",
            overwrite=True,
        )


def init_pyproject(name: str, description: typing.Optional[str] = None) -> None:
    raw_pyproject: str = Path("pyproject.toml").read_text()
    pyproject: tomlkit.TOMLDocument = tomlkit.parse(raw_pyproject)
    tool: tomlkit.items.Table = typing.cast(tomlkit.items.Table, pyproject["tool"])
    poetry: tomlkit.items.Table = typing.cast(tomlkit.items.Table, tool["poetry"])
    poetry["description"] = description if description else ""
    poetry["name"] = to_pip_name(name=name)
    with open(file="pyproject.toml", mode="w") as fp:
        raw_pyproject = tomlkit.dumps(data=pyproject)
        raw_pyproject = raw_pyproject.replace("template", name)
        raw_pyproject = TomlSort(input_toml=raw_pyproject).sorted()
        fp.write(raw_pyproject)


def substitute(name: str, filepath: Path) -> None:
    if filepath.exists():
        data: str = filepath.read_text()
        data = data.replace("template", name)
        filepath.write_text(data=data)


@click.command(name="init")
@click.option(
    "-p", "--template", type=click.Choice(choices=TEMPLATE_BRANCHES), default="main"
)
@click.option("-d", "--description", help="Description of the repository")
@click.option(
    "-g",
    "--gitignore",
    default=["python"],
    metavar="LANGUAGE",
    multiple=True,
    help="Specify a gitignore template for the repository",
)
@click.option("--private", is_flag=True, help="Make the new repository private")
@click.argument("name")
def cmd(
    template: str,
    description: typing.Optional[str],
    gitignore: tuple[str],
    private: bool,
    name: str,
) -> None:
    execute("git", "clone", "--branch", template, "--depth", "1", TEMPLATE_GIT, name)
    root: Path = Path(name)
    os.chdir(root)
    remove(path=".git")
    init_readme(name=name, description=description)
    init_gitignore(gitignore=gitignore)
    init_pyproject(name=name, description=description)
    for file in TEMPLATE_FILES:
        substitute(name=name, filepath=file)
    if Path("template").exists():
        move(src="template", dst=to_pip_name(name=name))
    execute("git", "init")
    execute("pre-commit", "install", "--install-hooks")
    execute("git", "add", "--all")
    execute("pre-commit", "run", "--all-files", check_returncode=False)
    execute("git", "add", "--all")
    execute("git", "commit", "--message", "fix: initial commit")
    execute(
        "gh",
        "repo",
        "create",
        "--homepage",
        f"https://{getpass.getuser()}.github.io/{name}/",
        "--private" if private else "--public",
        "--source",
        os.getcwd(),
    )
    if template == "python":
        cmd_secret.main(args=["PYPI_TOKEN"], standalone_mode=False)
    execute("git", "push", "--set-upstream", "origin", "main")
