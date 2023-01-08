#!/usr/bin/env python3
import os

import typer
import yaml
import subprocess

from typing import Optional

app = typer.Typer(help="Run git commands on multiple repositories", no_args_is_help=True)


class Output:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def header(text):
        print(f'{Output.HEADER}{text}{Output.ENDC}')

    @staticmethod
    def success(text):
        print(f'{Output.OKGREEN}{text}{Output.ENDC}')

    @staticmethod
    def error(text):
        print(f'{Output.FAIL}{text}{Output.ENDC}')


def get_targets(generate=False):
    if os.path.isfile('.gmc.yaml') and generate is False:
        with open('.gmc.yaml') as fr:
            data = yaml.safe_load(fr.read())

            return data['repositories']

    if generate is False:
        Output.error('Run "gmc build" to generate the repositories list file')

    all_dirs = os.listdir('.')
    repositories = []

    blacklist = [
        '.git',
        '.idea',
        'venv',
        'myv'
    ]
    for item in all_dirs:
        if os.path.isdir(item) and item not in blacklist:
            repositories.append(item)

    return sorted(repositories)

def run_git_command(command, directory):
    return subprocess.call(command, cwd=directory, shell=True)


@app.command('add')
@app.command('a')
def git_add(
        path: Optional[str] = typer.Argument('.')
):
    """
    Run git add in all directories
    :param path: 
    :return: 
    """
    targets = get_targets()

    for work_dir in targets:
        Output.header(f'{work_dir}::add')
        run_git_command(f'git add {path}', work_dir)


@app.command('status')
@app.command('st')
@app.command('s')
def git_status():
    """
    Run git status in all directories
    :param path:
    :return:
    """
    targets = get_targets()

    for work_dir in targets:
        Output.header(f'\n{work_dir}::status')
        run_git_command('git status', work_dir)


@app.command('init')
@app.command('i')
def git_init():
    """
    Run git init in directories
    :return:
    """
    targets = get_targets()

    for work_dir in targets:
        Output.header(f'{work_dir}::init')
        run_git_command('git init', work_dir)


@app.command('commit')
@app.command('c')
def git_commit(
        message: Optional[str] = typer.Argument('update code')
):
    """
    Run git commit in directories
    :return:
    """
    targets = get_targets()

    for work_dir in targets:
        Output.header(f'{work_dir}::commit')
        run_git_command(f'git commit -m "{message}"', work_dir)


@app.command('branch')
@app.command('b')
def git_branch(
    branch_name: Optional[str] = typer.Argument('dev')
):
    """
    Create a new branch in directories
    :return:
    """
    targets = get_targets()

    for work_dir in targets:
        Output.header(f'{work_dir}::create-branch')
        run_git_command(f'git checkout -b "{branch_name}"', work_dir)


@app.command('checkout')
@app.command('co')
def git_checkout(
    branch_name: Optional[str] = typer.Argument('master')
):
    """
    Run git checkout in directories to change the branches
    :return:
    """
    targets = get_targets()

    for work_dir in targets:
        Output.header(f'{work_dir}::create-branch')
        run_git_command(f'git checkout "{branch_name}"', work_dir)


@app.command('push')
@app.command('p')
def git_push(
    branch_name: Optional[str] = typer.Argument('')
):
    """
    Run git push in directories
    :return:
    """
    targets = get_targets()

    for work_dir in targets:
        Output.header(f'{work_dir}::push')
        if branch_name != '':
            branch_name = f'-u origin {branch_name}'
        run_git_command(f'git push "{branch_name}"', work_dir)


@app.command()
def build():
    """
    Build .gmc.yaml file with all directories in the current path
    :return:
    """
    Output.header('Generating .gmc.yaml file.')

    # @todo this is duplicate code, remove/fix later
    all_dirs = os.listdir('.')
    repositories = []

    blacklist = [
        '.git',
        '.idea',
        'venv',
        'myv'
    ]

    for item in all_dirs:
        if os.path.isdir(item) and item not in blacklist:
            repositories.append(item)
            Output.success(f'add directory: {item}')

    with open('.gmc.yaml', 'w') as fw:
        file_content = {
            'repositories': sorted(repositories)
        }
        fw.write(yaml.safe_dump(file_content))
        Output.success(f'Sorted and Done')
