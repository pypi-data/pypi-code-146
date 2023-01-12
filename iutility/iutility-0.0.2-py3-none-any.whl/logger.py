import logging
import typing

SKIPPED = logging.INFO + 1
EXECUTE = SKIPPED + 1
SUCCESS = EXECUTE + 1
TIPS = SUCCESS + 1


class Logger(logging.Logger):
    @staticmethod
    def escape(message: str) -> str:
        return message.replace(r"[", r"\[")

    def my_log(self, level: int, style: str, message: str, *args, **kwargs) -> None:
        message = self.escape(message)
        if self.isEnabledFor(level=level):
            self._log(
                level=level, msg=f"[{style}]" + message + "[/]", args=args, **kwargs
            )

    def skipped(self, msg: str, *args, **kwargs):
        self.my_log(
            level=SKIPPED, style="logging.level.skipped", message=msg, *args, **kwargs
        )

    def execute(self, msg: str, *args, **kwargs):
        self.my_log(
            level=EXECUTE, style="logging.level.execute", message=msg, *args, **kwargs
        )

    def success(self, msg: str, *args, **kwargs):
        self.my_log(
            level=SUCCESS, style="logging.level.success", message=msg, *args, **kwargs
        )

    def tips(self, msg: str, *args, **kwargs):
        self.my_log(
            level=TIPS, style="logging.level.tips", message=msg, *args, **kwargs
        )


def install_log_level(level: int, name: str):
    setattr(logging, name, level)
    logging._levelToName[level] = name
    logging._nameToLevel[name] = level
    pass


def install(level: int = logging.NOTSET):
    install_log_level(level=TIPS, name="TIPS")
    install_log_level(level=SUCCESS, name="SUCCESS")
    install_log_level(level=EXECUTE, name="EXECUTE")
    install_log_level(level=SKIPPED, name="SKIPPED")
    logging.setLoggerClass(Logger)
    if level > logging.CRITICAL:
        get_logger().disabled = True
    else:
        from rich.console import Console
        from rich.logging import RichHandler
        from rich.pretty import install as pretty_install
        from rich.theme import Theme
        from rich.traceback import install as traceback_install

        theme = Theme(
            {
                "logging.level.skipped": "dim",
                "logging.level.execute": "bold blue",
                "logging.level.success": "bold green",
                "logging.level.tips": "bold cyan",
            }
        )
        console = Console(theme=theme, stderr=True)
        pretty_install(console=console)
        traceback_install(console=console)
        logging.basicConfig(
            level=level,
            format="%(message)s",
            handlers=[RichHandler(console=console, markup=True)],
        )
    logging.root = get_logger()


def get_logger(name: str = "main") -> Logger:
    return typing.cast(Logger, logging.getLogger(name))
