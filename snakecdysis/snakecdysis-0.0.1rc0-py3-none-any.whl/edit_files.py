import click
from shutil import copyfile
from pathlib import Path


def __edit_tools(snake_installer, restore):
    if restore:
        if snake_installer.user_tools_path.exists():
            snake_installer.user_tools_path.unlink()
            click.secho(f"\n    Success remove your own tools_path.yaml on path '{snake_installer.user_tools_path}'", fg="yellow")
            click.secho(f"    {snake_installer.soft_name} used '{snake_installer.git_tools_path}' at default now !!\n\n", fg="bright_red")
        else:
            click.secho(f"    {snake_installer.soft_name} already used default tools_path.yaml '{snake_installer.git_tools_path}'!!\n\n", fg="red")
    else:
        if not snake_installer.user_tools_path.exists():
            snake_installer.user_tools_path.parent.mkdir(parents=True, exist_ok=True)
            copyfile(snake_installer.git_tools_path, snake_installer.user_tools_path)
        click.edit(require_save=True, extension='.yaml', filename=snake_installer.user_tools_path)
        click.secho(f"\n    Success install your own tools_path.yaml on path '{snake_installer.user_tools_path}'", fg="yellow")
        click.secho(f"    {snake_installer.soft_name} used '{snake_installer.user_tools_path}' at default now !!\n\n", fg="bright_red")


def __create_config(snake_installer, configyaml):
    configyaml = Path(configyaml)
    configyaml.parent.mkdir(parents=True, exist_ok=True)
    copyfile(snake_installer.git_config_path.as_posix(), configyaml.as_posix())
    click.edit(require_save=True, extension='.yaml', filename=configyaml.as_posix())
    click.secho(f"\n    Success create config file on path '{configyaml}'\n    add to command:", fg="yellow")
    mode = snake_installer.install_mode
    click.secho(f"    {snake_installer.soft_name} {'run_cluster' if mode == 'cluster' else 'run_local'} --config {configyaml}\n\n", fg="bright_blue")


def __edit_cluster_config(snake_installer):
    f"""Edit file on {snake_installer.user_cluster_config}"""
    snake_installer.user_cluster_config.parent.mkdir(parents=True, exist_ok=True)
    if not snake_installer.user_cluster_config.exists():
        copyfile(snake_installer.git_cluster_config.as_posix(), snake_installer.user_cluster_config.as_posix())
    click.edit(require_save=True, extension='.yaml', filename=snake_installer.user_cluster_config.as_posix())
    click.secho(f"\n    See '{snake_installer.DOCS}' to adapt on your cluster", fg="yellow")
    click.secho(f"\n    Success edit cluster_config file on path '{snake_installer.user_cluster_config}'", fg="yellow")
