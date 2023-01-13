import os
import sys

import click
from click import ClickException, Choice

from pyqalx import QalxSession
from pyqalx.config import UserConfig, BotConfig
from pyqalx.core.errors import (
    QalxConfigProfileNotFound,
    QalxConfigFileNotFound,
    QalxConfigError,
    QalxAPIResponseError,
    QalxError,
)
from qalxcli import cli_types
from qalxcli.utils import generate_key_file


@click.group(chain=True)
@click.option(
    "-u",
    "--user-profile",
    help="User profile name in .qalx.",
    default=UserConfig.default,
)
@click.option(
    "-b",
    "--bot-profile",
    help="Bot profile name in .bots.",
    default=BotConfig.default,
)
@click.version_option()
@click.pass_context
def qalx(ctx, user_profile, bot_profile):
    """Command line interface to qalx."""
    ctx.ensure_object(dict)
    ctx.obj["USER_PROFILE"] = user_profile
    ctx.obj["BOT_PROFILE"] = bot_profile
    sys.path.append(os.getcwd())


@qalx.command("configure")
@click.option("--user/--no-user", default=True)
@click.option("--bot/--no-bot", default=True)
@click.argument("extra", nargs=-1, type=cli_types.QALX_DICT)
@click.pass_context
def configure(ctx, user, bot, extra):
    """
    Configures the .qalx and .bots config files.
    Usage:

    `qalx configure` - configures user and bot default profiles

    `qalx --user-profile=dev configure` - configures dev user profile and
    default bot profile

    `qalx --bot-profile=dev configure --no-user` - only configures bot dev
    profile.  Doesn't configure user profile

    `qalx configure --no-bot customkey=customvalue customkey2=customvalue2`
    - configures user profile with two extra key/values pairs on the config
    """

    if not user and not bot:
        raise ClickException(
            "`user` or `bot` must be specified otherwise no "
            "config files can be created.  Either call "
            "without any arguments or only use a "
            "single `--no-user` or `--no-bot` switch"
        )

    user_profile = ctx.obj["USER_PROFILE"]
    bot_profile = ctx.obj["BOT_PROFILE"]
    check_existing = []

    if user:
        check_existing.append((UserConfig, user_profile, "user"))
    if bot:
        check_existing.append((BotConfig, bot_profile, "bot"))

    for ConfigClass, profile_name, config_type in check_existing:
        # If the profiles already exist we just exit.  It's up to the user
        # to make any changes manually to the profile file - otherwise we risk
        # parsing the file incorrectly and overwriting data the user wants to
        # keep
        try:
            ConfigClass().from_inifile(profile_name)
            config_path = ConfigClass.config_path()
            raise ClickException(
                f"`{profile_name}` profile for config stored "
                f"at `{config_path}` "
                f"already exists.  To make changes you must "
                f"edit the config file directly or specify a "
                f"`--no-{config_type}` flag"
            )
        except (QalxConfigProfileNotFound, QalxConfigFileNotFound):
            # QalxConfigProfileNotFound: The specific profile could not be
            #                            found in the given ConfigClass file
            # QalxConfigFileNotFound: The specific file could not be found
            #                         for the given ConfigClass
            pass

    config_items = {k.upper(): v for d in extra for k, v in d.items()}

    if user:
        # Get the token
        value = click.prompt("qalx Token", type=str)
        config_items["TOKEN"] = value

        region = click.prompt(
            "region",
            default=UserConfig.DEFAULT_REGION,
            type=Choice(choices=UserConfig.REGION_MAPPING["aws"].keys()),
        )
        config_items["REGION"] = UserConfig.REGION_MAPPING["aws"][region]

        # Get the key file for encryption
        key_file = config_items.get("KEYFILE")
        if key_file is None:
            if click.confirm("Do you have an encryption key file?"):
                key_file = click.prompt(
                    "Enter full path to encryption key file"
                )
            elif click.confirm(
                "Do you want to generate an encryption key file?"
            ):
                key_file = generate_key_file()
            if key_file is not None:
                config_items["KEYFILE"] = key_file
        try:
            UserConfig.configure(user_profile, config_items)
        except QalxConfigError as exc:
            raise ClickException(exc)
    if bot:
        try:
            BotConfig.configure(bot_profile)
        except QalxConfigError as exc:
            raise ClickException(exc)


@qalx.command("generate-encryption")
def generate_encryption():
    """
    Generates an encryption key file for the user prints out the path if it does
    so successfully
    """
    key_file_path = generate_key_file()
    click.echo(
        f"\nThe encryption key file has been generated in:\n{key_file_path}\n"
        + "The qalx configuration file must be updated manually for the new "
        + "file to be used, by adding the following line under the appropriate "
        + f"profile:\n\nKEYFILE={key_file_path}"
    )


@qalx.command("download")
@click.argument("guid")
@click.option(
    "-d",
    "--directory",
    type=cli_types.DIR_PATH_EXISTING,
    help="The directory where the file will be downloaded.",
    default=None,
)
@click.option(
    "-e",
    "--entity-type",
    type=cli_types.FILE_ENTITY_TYPE,
    help="The type of entity to download a file for.",
    default="item",
)
@click.pass_context
def download(ctx, guid, directory, entity_type):
    """
    Downloads a file for the specified entity type and guid. The download
    directory can also be specified, otherwise the default location from the
    qalx config file will be used
    """
    qalx_session = QalxSession(profile_name=ctx.obj["USER_PROFILE"])
    if directory is None:
        directory = qalx_session.config["DOWNLOAD_DIR"]
        # The directory from the config might not exist
        if not os.path.exists:
            os.mkdir(directory)
    try:
        entity = getattr(qalx_session, entity_type).get(guid)
    except QalxAPIResponseError as exc:
        msg = f"{entity_type} with guid: {guid} not found:\n\n{exc}"
        raise ClickException(msg)
    try:
        entity.save_file_to_disk(directory)
    except QalxError as exc:
        raise ClickException(exc)
