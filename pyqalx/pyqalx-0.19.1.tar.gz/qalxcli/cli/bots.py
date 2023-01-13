import logging

import click
from click import ClickException, types

from pyqalx import QalxSession
from pyqalx.config import UserConfig, BotConfig
from pyqalx.core.errors import QalxError
from pyqalx.core.utils import _msg_user

from .. import cli_types
from ..cli.qalx import qalx
from ..utils import (
    TerminateBotTabulation,
    StopBotTabulation,
    ResumeBotTabulation,
    BotTabulation,
)


@qalx.command("bot-start")
@click.option(
    "-p",
    "--processes",
    type=cli_types.POSITIVE_INT,
    help="The number of workers to spawn in the bot.",
    default=1,
)
@click.option(
    "--skip-ini/--no-skip-ini",
    help="Should the bot use the profiles on disk?",
    default=False,
)
@click.argument("target", type=cli_types.BOT_IMPORT)
@click.option(
    "-q",
    "--queue-name",
    help="The name of the queue this bot should read messages from",
    required=True,
)
@click.option(
    "--qalx-session-class",
    type=cli_types.QALX_SESSION_IMPORT,
    help="The import path of a custom QalxSession class in the format "
    "`dotted.path.to:MyQalxSessionClass`",
    default=None,
)
@click.option(
    "--user-config-class",
    type=cli_types.USER_CONFIG_IMPORT,
    help="The import path of a custom UserConfigClass class in the format "
    "`dotted.path.to:MyUserConfigClass`",
    default=None,
)
@click.option(
    "--bot-config-class",
    type=cli_types.BOT_CONFIG_IMPORT,
    help="The import path of a custom BotConfigClass class in the format "
    "`dotted.path.to:MyBotConfigClass`",
    default=None,
)
@click.option(
    "--entity-class",
    type=cli_types.QALX_ENTITY_IMPORT,
    help="The import path of a custom QalxEntity class in the format "
    "`dotted.path.to:MyQalxEntityClass`",
    multiple=True,
)
@click.option(
    "--stop",
    is_flag=True,
    help="If provided the workers will be stopped immediately after startup",
)
@click.option(
    "--meta",
    type=cli_types.QALX_DICT,
    help=(
        "Key value pair of the format <key>=<value>, for example: "
        + "--meta <key>=<value>. Multiple meta arguments can be passed"
    ),
    multiple=True,
)
@click.option(
    "--workflow",
    type=click.STRING,
    help=(
        "The name of another bot to pass a message to once all step "
        + "functions have been completed on this bot"
    ),
    multiple=True,
)
@click.pass_context
def start(
    ctx,
    target,
    queue_name,
    processes,
    skip_ini,
    qalx_session_class,
    user_config_class,
    bot_config_class,
    entity_class,
    stop,
    meta,
    workflow,
):
    """
    Start the bot at TARGET

    This is the import path with a colon followed by the variable name
    of the bot. e.g. `my_qalx.my_bot:bot`
    """
    click.echo(
        f"Starting {target.name} reading from {queue_name} with"
        f" {processes} workers."
    )
    meta = {k: v for d in meta for k, v in d.items()} if meta else None
    user_profile = ctx.obj.get("USER_PROFILE", UserConfig.default)
    bot_profile = ctx.obj.get("BOT_PROFILE", BotConfig.default)
    qalx_session = QalxSession(
        profile_name=ctx.obj["USER_PROFILE"], skip_ini=skip_ini
    )
    try:
        target.start(
            queue_name=queue_name,
            user_profile_name=user_profile,
            bot_profile_name=bot_profile,
            processes=processes,
            skip_ini=skip_ini,
            qalx_session_class=qalx_session_class,
            user_config_class=user_config_class,
            bot_config_class=bot_config_class,
            entity_classes=list(entity_class),
            stop=stop,
            meta=meta,
            workflow=list(workflow),
        )
    except QalxError as exc:
        _msg_user(
            title="start",
            msg=str(exc),
            log=qalx_session.log,
            level=logging.ERROR,
        )
        _msg_user(msg="Bot Start Failed", log=qalx_session.log)


@qalx.command("bot-terminate")
@click.argument("name")
@click.pass_context
def terminate_bot(ctx, name):
    """Shutdown the bot named NAME"""
    qalx_session = QalxSession(
        profile_name=ctx.obj.get("USER_PROFILE", UserConfig.default)
    )
    bot_tabulation = TerminateBotTabulation(qalx_session, name)
    bot_to_kill = bot_tabulation.get_entity_or_display()
    if bot_to_kill:
        # Finally, terminate the bot
        try:
            qalx_session.bot.terminate(bot_to_kill)
        except QalxError as exc:
            _msg_user(
                title="terminate",
                msg=str(exc),
                log=qalx_session.log,
                level=logging.ERROR,
            )
            _msg_user(msg="Bot Terminate Failed", log=qalx_session.log)
        else:
            click.echo(
                f"Terminate signal sent for `{bot_to_kill.name} "
                f"({bot_to_kill.host.get('platform')})`.  Workers may take "
                f"some time to terminate"
            )


@qalx.command("bot-stop")
@click.argument("name")
@click.pass_context
def stop_bot(ctx, name):
    """Stop the bot named NAME.

    All workers to stop pulling jobs from the queue.
    """
    qalx_session = QalxSession(
        profile_name=ctx.obj.get("USER_PROFILE", UserConfig.default)
    )
    bot_tabulation = StopBotTabulation(qalx_session, name)
    bot_to_stop = bot_tabulation.get_entity_or_display()

    if bot_to_stop:
        try:
            qalx_session.bot.stop(bot_to_stop)
        except QalxError as exc:
            _msg_user(
                title="stop",
                msg=str(exc),
                log=qalx_session.log,
                level=logging.ERROR,
            )
            _msg_user(msg="Bot Stop Failed", log=qalx_session.log)
        else:
            click.echo(f"Stopping {name}.")


@qalx.command("bot-resume")
@click.argument("name")
@click.pass_context
def resume_bot(ctx, name):
    """Resume the bot named NAME.

    All workers to start pulling jobs from the queue.
    """
    qalx_session = QalxSession(
        profile_name=ctx.obj.get("USER_PROFILE", UserConfig.default)
    )
    bot_tabulation = ResumeBotTabulation(qalx_session, name)
    bot_to_resume = bot_tabulation.get_entity_or_display()
    if bot_to_resume:
        try:
            qalx_session.bot.resume(bot_to_resume)
        except QalxError as exc:
            _msg_user(
                title="resume",
                msg=str(exc),
                log=qalx_session.log,
                level=logging.ERROR,
            )
            _msg_user(msg="Bot Resume Failed", log=qalx_session.log)
        else:
            click.echo(f"Resuming {name}.")


@qalx.command("bot-info")
@click.argument("name")
@click.pass_context
def bot_info(ctx, name):
    """Print info about the bot named NAME."""
    qalx_session = QalxSession(
        profile_name=ctx.obj.get("USER_PROFILE", UserConfig.default)
    )
    try:
        bot_tabulation = BotTabulation(qalx_session, name, tabulate_single=True)
        bot_tabulation.get_entity_or_display()
    except QalxError as exc:
        _msg_user(
            title="info",
            msg=str(exc),
            log=qalx_session.log,
            level=logging.ERROR,
        )
        _msg_user(msg="Bot Info Failed", log=qalx_session.log)


@qalx.command("workers-terminate")
@click.argument("bot_name")
@click.argument("number", type=types.INT)
@click.pass_context
def terminate_workers(ctx, bot_name, number):
    """Terminate NUMBER of workers on bot named BOT_NAME."""
    qalx_session = QalxSession(
        profile_name=ctx.obj.get("USER_PROFILE", UserConfig.default)
    )
    bot_tabulation = TerminateBotTabulation(qalx_session, bot_name)
    bot_to_kill = bot_tabulation.get_entity_or_display()
    if bot_to_kill:
        if number > len(bot_to_kill.workers):
            raise ClickException(
                f"{number} is more than the number of workers on {bot_name}"
                f" ({len(bot_to_kill.workers)})"
            )
        for n in range(number):
            try:
                qalx_session.worker.terminate(
                    bot_to_kill.workers[n], bot_entity=bot_to_kill
                )
            except QalxError as exc:
                _msg_user(
                    title="workers terminate",
                    msg=str(exc),
                    log=qalx_session.log,
                    level=logging.ERROR,
                )
                _msg_user(msg="Worker Terminate Failed", log=qalx_session.log)
            else:
                click.echo(f"Terminated worker number {n + 1}.")
