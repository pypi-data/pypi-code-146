#!/usr/bin/env python
import click

from . import create


@click.group()
def cli():
    pass


@cli.command()
@click.argument('name', nargs=1)
@click.option('-m', '--model_dir', type=str, default=None, help='[optional] Directory where your models are.')
def new(name, model_dir):
    create.main(name, model_dir)


@cli.command()
@click.option('-n', '--name')
def greet(name):
    print(name)


if __name__ == '__main__':
    cli()
