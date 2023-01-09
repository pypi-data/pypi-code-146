import argparse
import logging
import sys
from typing import List, Optional, TextIO

import yaml

from .job import Job
from .parser import parse_recipe


def setup_logger(debug: bool = False) -> logging.Logger:
    logger = logging.getLogger(__name__)
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)
    fmt = logging.Formatter(logging.BASIC_FORMAT)
    ch = logging.StreamHandler(sys.stderr)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    return logger


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--recipefile", "-r", type=argparse.FileType("r"), required=True
    )
    parser.add_argument("--envfile", "-e", type=argparse.FileType("r"))
    parser.add_argument("--task", "-t", type=str, nargs="+", default=[])
    parser.add_argument("--loop", "-l", type=bool, default=False)
    parser.add_argument("--debug", type=bool, default=False)
    parser.add_argument("--show", type=bool, default=False)
    parser.add_argument("--duration", type=float, default=0.0)
    argv = parser.parse_args()

    main_(
        debug=argv.debug,
        envfile=argv.envfile,
        recipefile=argv.recipefile,
        task_names=argv.task,
        only_show=argv.show,
        cooldown=argv.duration,
    )


def main_(
    *,
    debug: bool,
    envfile: Optional[TextIO],
    recipefile: TextIO,
    task_names: List[str],
    only_show: bool = False,
    cooldown: float = 0.0,
    loop: bool = False
) -> None:
    setup_logger(debug)
    if envfile is not None:
        envs = yaml.safe_load(envfile)
    else:
        envs = {}

    recipe = parse_recipe(recipefile, envs)
    job = Job.from_job_directive(recipe)
    if task_names:
        job = job.filter_task_by_names(task_names)

    if only_show:
        for task in job.tasks:
            print(task.name)
        return
    job.run(cooldown=cooldown, loop=loop)


if __name__ == "__main__":
    main()
