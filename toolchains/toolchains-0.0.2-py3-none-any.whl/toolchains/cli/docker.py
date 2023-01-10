# -*- coding: utf-8 -*-
import sys
import json
import argparse
from pawnlib.typing import generate_number_list, Counter
from pawnlib.config.globalconfig import pawnlib_config as pawn
from pawnlib.output import *
from pawnlib.asyncio import AsyncTasks
from toolchains.docker import AsyncDocker, run_container, run_dyn_container
from PyInquirer import prompt, Separator

from rich.prompt import Confirm, FloatPrompt, Prompt, PromptBase
from rich.syntax import Syntax

from jinja2 import Template
from pathlib import Path
from importlib.machinery import SourceFileLoader
import os
import configparser


__version__ = "0.0.1"

EXEC_PATH = os.getcwd()


def get_parser():
    parser = argparse.ArgumentParser(description='Command Line Interface for docker')
    parser = get_arguments(parser)
    return parser


def get_arguments(parser):
    parser.add_argument(
        'command',
        choices=['dc', 'create', 'create_or_replace', 'delete', 'start', 'stop', 'init'],
        help='')
    parser.add_argument('-s', '--unixsocket', metavar='unixsocket', help=f'unix domain socket path ',
                        default="/var/run/docker.sock")
    parser.add_argument('-d', '--debug', action='store_true', help=f'debug mode. (default: False)', default=False)
    parser.add_argument('-c', '--count', metavar="container count", type=int, help=f'container count', default=30)
    parser.add_argument('--max_at_once', metavar="max_at_once count", type=int, help=f'max_at_once count', default=50)
    parser.add_argument('--max_per_second', metavar="max_per_second count", type=int, help=f'max_per_second count', default=50)
    parser.add_argument('-n', '--name', metavar="container name", type=str, help=f'container prefix name ', default=None)
    parser.add_argument('-i', '--image', metavar="image name", type=str, help=f'docker image name ', default=None)

    # parser.add_argument('-f', '--file', type=argparse.FileType('r'), help="container source code")
    parser.add_argument('-f', '--file', type=str, help="import the container source code", default='dynamic_import.py')
    parser.add_argument('--config', type=str, help="import the config file", default=f'{EXEC_PATH}/config.ini')
    parser.add_argument('-t', '--target', type=str, help="target", default=None)
    return parser


def initialize(args):
    pawn.set(PAWN_CONFIG_FILE=args.config)
    pawn.console.log(f"os.cwd => {EXEC_PATH}")
    pwn = pawn.conf()
    pawn_config = pawn.to_dict().get('PAWN_CONFIG')

    default_image = {
        "docker_planet": "jinwoo/planet",
        "docker_echo": "jmalloc/echo-server"
    }
    if args.command == "init":
        pawn.console.log("Generate the sample files for docker container")
        template_dir = f"{os.path.dirname(__file__)}/templates"

        template_question = [
            {
                'type': 'list',
                'name': 'category',
                'message': 'What do you want to template?',
                'choices': [tmpl_file.replace(".tmpl", "") for tmpl_file in os.listdir(template_dir) if tmpl_file.endswith('.tmpl')],
            },
            {
                'type': 'input',
                'name': 'target_list',
                'message': 'What\'s the target list?',
                # 'default': "[]"
                'default': lambda x: f'Counter(start=10000, stop=10000+args.count, convert_func=str)' if "docker_echo" in x['category'] else "[]"
            },
            {
                'type': 'input',
                'name': 'filename',
                'message': 'What\'s the filename?',
                'default': lambda x: x['category']
            },
            {
                'type': 'input',
                'name': 'image',
                'message': 'What\'s your image name?',
                'default': lambda x: default_image.get(x['category'])
            },
            {
                'type': 'input',
                'name': 'container_name',
                'message': 'What\'s your container name?',
                'default': lambda x: x['category']
            },
        ]

        answers = prompt(template_question)
        template_file = f"{template_dir}/{answers['category']}.tmpl"
        template = open_file(f"{template_file}")

        templated_dict = Template(template).render(
            **answers
        )

        syntax = Syntax(templated_dict, "python")
        pawn.console.rule(answers['category'])
        pawn.console.print(syntax)
        pawn.console.rule("")

        check_file_overwrite(filename=f"{answers['category']}.py")
        write_file(filename=f"{answers['category']}.py", data=templated_dict, permit="660")

        check_file_overwrite(filename=args.config)
        config = configparser.ConfigParser()
        config['default'] = {
            "image": answers['image'],
            "name": answers['container_name'],
            "file": f"{EXEC_PATH}/{answers['filename']}.py",
            "target": answers['target_list'],
        }
        with open(args.config, 'w') as configfile:
            config.write(configfile)

    if pawn_config:
        pawn.console.log(f"Found config file => '{pwn.PAWN_CONFIG_FILE}'")
        pawn.console.log(f"pawn_config={pawn_config}")

        if not args.image:
            args.image = pawn_config['default']['image']

        if not args.name:
            args.name = pawn_config['default']['name']

        # if not args.target and pawn_config['default'].get('target_list'):
        args.target = pawn_config['default'].get('target')

        args.file = pawn_config['default'].get('file')

    if args.image and ":" not in args.image:
        args.image = f"{args.image}:latest"

    pawn.set(args=args)

    if is_file(args.file):
        _file = Path(args.file)
        module_name = _file.stem
        # module_name = args.file.replace(".py", "")
        pawn.console.log(f"module_name={module_name}, file={args.file}")
        args.module = SourceFileLoader(module_name, args.file).load_module()
        pawn.console.log(f"[bold]Load a '{module_name}' from {args.module}")
    return args


def main():
    parser = get_parser()
    args, unknown = parser.parse_known_args()
    args = initialize(args)

    pawn.console.log(f"args={args}, unknown={unknown}")

    with AsyncDocker(
            client_options=dict(
                url=f"unix://{args.unixsocket}"
            ),
            # client=aiodocker.Docker()
            max_at_once=args.max_at_once,
            max_per_second=args.max_per_second,
            count=args.count,
            container_name=args.name
            # filters={"Names": f"{args.name}.*"}
    ) as docker:
        if args.image:
            if not docker.find_image(image=args.image):
                pawn.console.log(f"Pulling image - {args.image}")
                docker.pull_image(args.image)
        else:
            pawn.console.log("[red] image not found")

        if args.command == "create":
            async_tasks = AsyncTasks(args=args, max_at_once=args.max_at_once, max_per_second=args.max_per_second)
            async_tasks.generate_tasks(
                target_list=Counter(start=10000, stop=10000+args.count, convert_func=str),
                function=run_container,
                **{"args": args}
            )
            async_tasks.run()

        elif args.command == 'dc':
            try:
                args.target = json.loads(args.target)
            except:
                pawn.console.log(f"[green] {args.target} {type(args.target)}")

            async_tasks = AsyncTasks(args=args, max_at_once=args.max_at_once, max_per_second=args.max_per_second)
            async_tasks.generate_tasks(
                target_list=args.module.target_list or args.target,
                function=args.module.main,
                **{"args": args}
            )
            async_tasks.run()
        else:
            docker.control_container(method=args.command, filters={"Names": f"{args.name}.*"}, all=True)

        if args.command == "create_or_replace":
            docker.control_container(method="start", filters={"Names": f"{args.name}.*"}, all=True)


if __name__ == "__main__":
    main()
