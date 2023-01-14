import click
from create_files import *
import sqlite3
# from celestis.read_models import *
from model.read_models import *
import os

@click.command()
@click.argument("subcommand", required=True)
def celestis(subcommand):
    if subcommand == 'create-files':
        project_name = str(input("What is your project name?"))
        create_app(project_name)
        click.echo("Cool! Your project files have been created")
    if subcommand == 'create-db':
        conn = sqlite3.connect("db.sqlite3")
        conn.close()
        click.echo("SQLite file has been created in your project folder!")
    if subcommand == 'update-db':
        read_db(os.getcwd())
        click.echo("Process is complete")