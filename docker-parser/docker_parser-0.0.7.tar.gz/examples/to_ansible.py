import sys
import os

sys.path.insert(0, os.path.join(
    os.path.dirname(__file__),
    '..'
))

import argparse

import docker_parser
import yaml

ANSIBLE_PLAY = {
    'hosts': 'all',
    'vars': {
    },
    'tasks': []
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dockerfile', help="Dockerfile to attempt to translate")
    parser.add_argument('path', help="path where to save ansible")
    args = parser.parse_args()

    with open(args.dockerfile, 'r') as src:
        dockerfile = docker_parser.parser.Parser.loads(src.read())
    
    ANSIBLE_PLAY['vars']['environment'] = dockerfile.stages[-1].env

    for cmd in dockerfile.stages[-1].commands:
        if cmd.command.lower() in ("copy", 'add'):
            ANSIBLE_PLAY['tasks'].append({
                'copy': {
                    'src': "{{ item }}",
                    'dest': cmd.destination
                },
                'with_items': cmd.sources,
                'environment': "{{ environment }}"
            })
        elif cmd.command.lower() == "run":
            ANSIBLE_PLAY['tasks'].append({
                'shell': {
                    'cmd': cmd.arg
                },
                'environment': "{{ environment }}"
            })
    with open(args.path, 'w') as dst:
        yaml.dump([ANSIBLE_PLAY], dst)