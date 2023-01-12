import click
from app.aitest_application import *


@click.group()
def main():
    """  The  aitest  Command  Line  Interface is a unified tool to manage your aitest
         services.

        To see help text, you can run:

        aitest --help\n
        aitest <command> --help\n
        aitest <command> <subcommand> --help\n

    """

#adding subcommands 
main.add_command(configure)
main.add_command(run)
main.add_command(status)
