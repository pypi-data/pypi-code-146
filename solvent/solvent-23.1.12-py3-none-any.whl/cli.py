import itertools
import pdb
import random
import sys
from bdb import BdbQuit

import log
import pomace
import typer
from bullet import Bullet

from .scripts import Script


def run():
    typer.run(cli)


def cli(
    names: list[str] = typer.Argument(
        None,
        metavar="[SCRIPT SCRIPT ...]",
        help="Names of one or more scripts to run in a loop",
    ),
    duration: int = typer.Option(
        5 * 60, metavar="SECONDS", help="Amount of time to spend in each script"
    ),
    dev: bool = typer.Option(False, help="Enable development mode"),
):
    log.reset()
    log.init(debug=dev)
    log.silence("datafiles", allow_warning=True)

    scripts = {}
    for cls in Script.__subclasses__():
        script = cls()  # type: ignore
        scripts[script.name] = script

    if "all" in names:
        log.info("Running all scripts")
        names = [k for k, v in scripts.items() if (not v.SKIP or duration < 60)]
        random.shuffle(names)
    elif names and all(name in scripts.keys() for name in names):
        pass
    else:
        choices = sorted(cls().title for cls in Script.__subclasses__())  # type: ignore
        cli = Bullet(
            prompt="\nSelect a script to run:",
            bullet=" ● ",
            choices=choices,
            return_index=True,
        )
        if pomace.settings.action > len(scripts) - 1:
            pomace.settings.action = 0
        cli.pos = pomace.settings.action
        value, pomace.settings.action = cli.launch()
        names = [value.replace(" ", "").lower()]
        pomace.prompts.linebreak(force=True)

    try:
        import caffeine
    except ImportError:
        log.warn(f"Display sleep cannot be disabled on {sys.platform}")
    else:
        caffeine.on(display=True)

    pomace.utils.locate_models()
    if not dev:
        pomace.freeze()

    try:
        _run(scripts, names, duration, dev)
    except (KeyboardInterrupt, BdbQuit):
        pass
    except Exception as e:
        log.error(e)
        if dev:
            _type, _value, traceback = sys.exc_info()
            pdb.post_mortem(traceback)
        else:
            raise e from None


def _run(scripts: dict, names: list, duration: int, dev: bool):
    if len(names) > 1:
        for count in itertools.count(start=1):
            for name in names:
                scripts[name].loop(duration, dev=dev)
            log.info(f"Completed {count} loops")
    else:
        scripts[names[0]].loop(dev=dev)
