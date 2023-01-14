import getpass
import os
import typing
from pathlib import Path

import click
import tomlkit
import tomlkit.items
from ishutils import download, move, remove, run
from toml_sort.tomlsort import TomlSort

from .define import (
    GITIGNORE_API,
    INITIAL_COMMIT,
    TEMPLATE_BRANCHES,
    TEMPLATE_FILES,
    TEMPLATE_GIT,
)
from .secret import cmd as cmd_secret


def package_name(name: str) -> str:
    return name.lower().replace("-", "_")


def init_readme(name: str, description: typing.Optional[str] = None) -> None:
    with open(file="README.md", mode="w") as fp:
        lines: list[str] = [f"# {name}"]
        if description:
            lines.append("")
            lines.append(description)
        fp.writelines([line + "\n" for line in lines])


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
    poetry["name"] = name
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
    run("git", "clone", "--branch", template, "--depth", "1", TEMPLATE_GIT, name)
    root: Path = Path(name)
    os.chdir(root)
    remove(path=".git")
    init_readme(name=name, description=description)
    init_gitignore(gitignore=gitignore)
    init_pyproject(name=name, description=description)
    for file in TEMPLATE_FILES:
        substitute(name=name, filepath=file)
    if Path("template").exists():
        move(src="template", dst=package_name(name=name))
    run("git", "init")
    run("pre-commit", "install", "--install-hooks")
    run("git", "add", "--all")
    run("pre-commit", "run", "--all-files", check_returncode=False)
    run("git", "add", "--all")
    run("git", "commit", "--message", INITIAL_COMMIT)
    run(
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
        cmd_secret.main(args=["pypi"], standalone_mode=False)
    run("git", "push", "--set-upstream", "origin", "main")
