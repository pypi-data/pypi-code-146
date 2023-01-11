import logging
from typing import Any, Callable, ClassVar, List

from click import Command, Context, Group
from click.exceptions import Abort, ClickException, Exit
from sentry_sdk.api import push_scope

from sym.shared.cli.data.global_options_base import GlobalOptionsBase
from sym.shared.cli.errors import UnknownError, get_active_env_vars
from sym.shared.cli.helpers.tee import Tee, TeeStdErr, TeeStdOut
from sym.shared.cli.helpers.util import is_prod_mode

from . import segment


class AutoTagCommand(Command):
    """
    A command where each invocation sets the Sentry tag with the
    command's name automatically. Additionally, any CliErrors
    raised from the command are logged.
    """

    def invoke(self, ctx: Context) -> Any:
        segment.track(
            "Command Executed",
            global_options=ctx.find_object(GlobalOptionsBase),
            command=ctx.info_name,
            options=ctx.obj.to_dict(),
        )
        with push_scope() as scope:
            scope.set_tag("command", ctx.info_name)
            scope.set_extra("options", ctx.obj.to_dict())
            return super().invoke(ctx)

    def format_epilog(self, ctx, formatter):
        if not self.epilog:
            formatter.write(get_active_env_vars())
        super().format_epilog(ctx, formatter)


class SymGroup(Group):
    """
    A group where any defined commands automatically use
    AutoTagCommand.
    """

    tees: ClassVar[List[Tee]] = []
    instances = []

    def __init__(self, *args: Any, **attrs: Any) -> None:
        super().__init__(*args, **attrs)
        SymGroup.instances.append(self)

    def __del__(self):
        self.__class__.reset_tees()

    @classmethod
    def reset_tees(cls):
        for tee in cls.tees:
            tee.close()
        cls.tees = []

    def invoke(self, ctx: Context) -> Any:
        if log_dir := ctx.params.get("log_dir"):
            # Don't register exit handler so exceptions are teed.
            # Instead, __del__ will be called when the program exits.
            self.__class__.tees.extend((TeeStdOut(log_dir), TeeStdErr(log_dir)))
            logging_filename = Tee.path_for_fd(log_dir, "logging")
        else:
            logging_filename = None

        if ctx.params.get("debug"):
            logging.basicConfig(level=logging.DEBUG, filename=logging_filename)
            logging.getLogger("segment").setLevel(logging.WARNING)
            logging.getLogger("backoff").setLevel(logging.WARNING)
        else:
            logging.getLogger("segment").setLevel(logging.CRITICAL)
            logging.getLogger("backoff").setLevel(logging.CRITICAL)

        try:
            return super().invoke(ctx)
        except (ClickException, Abort, Exit):
            raise
        except KeyboardInterrupt:
            pass
        except Exception as e:
            if not is_prod_mode() or ctx.params.get("debug"):
                raise e
            raise UnknownError(e)

    def command(
        self, *args: Any, cls=None, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], AutoTagCommand]:
        return super().command(*args, **kwargs, cls=cls or AutoTagCommand)  # type: ignore
