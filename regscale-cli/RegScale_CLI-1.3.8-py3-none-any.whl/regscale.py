#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""standard python imports"""
import os
import sys

import click
from rich.console import Console

import app.healthcheck as hc
import app.login as lg

############################################################
# Versioning
############################################################
from app._version import __version__
from app.ad import ad
from app.application import Application
from app.cisa import cisa
from app.jira import jira
from app.logz import create_logger
from app.migrations import migrations
from app.oscal import oscal
from app.servicenow import servicenow
from app.tenable import tenable
from app.wiz import wiz
from app.reminder import reminder
from app.defender import defender
from app.encrypt import JH0847, IOA21H98, YO9322
from app.comparison import compare
from app.evidence import evidence

############################################################
# CLI Command Definitions
############################################################


console = Console()

app = Application()

logger = create_logger()


@click.group()
def cli():
    """
    Welcome to the RegScale CLI client app!
    """


# About function
@cli.command()
def about():
    """Provides information about the CLI and its current version."""
    banner()
    console.print("[red]RegScale[/red] CLI Version: " + __version__)
    console.print("Author: J. Travis Howerton (thowerton@regscale.com)")
    console.print("Copyright: RegScale Incorporated")
    console.print("Website: https://www.regscale.com")
    console.print("Read the CLI Docs: https://regscale.com/documentation/cli-overview")
    java = app.get_java()
    matches = ["not found", "internal or external"]
    if not any(x in java for x in matches):
        console.print(f"Java: {java}")


def banner():
    """RegScale logo banner"""
    txt = """
\t[#10c4d3] .';;;;;;;;;;;;;[#14bfc7];;;;;;;;;;;;,'..
\t[#10c4d3].:llllllllllllll[#14bfc7]lllllllllllllllc:'.
\t[#10c4d3].cliclicliclicli[#14bfc7]clicliclicliclooool;.
\t[#10c4d3].cliclic###################;:looooooc'
\t[#05d1b7].clicli,                     [#15cfec].;loooool'
\t[#05d1b7].clicli,                       [#18a8e9].:oolloc.
\t[#05d1b7].clicli,               [#ef7f2e].,cli,.  [#18a8e9].clllll,
\t[#05d1b7].clicli.             [#ef7f2e].,oxxxxd;  [#158fd0].:lllll;
\t[#05d1b7] ..cli.            [#f68d1f]';cdxxxxxo,  [#18a8e9].cllllc,
\t                 [#f68d1f].:odddddddc.  [#1b97d5] .;ccccc:.
\t[#ffc42a]  ..'.         [#f68d1f].;ldddddddl'  [#0c8cd7].':ccccc:.
\t[#ffc42a] ;xOOkl.      [#e9512b]'coddddddl,.  [#0c8cd7].;::::::;.
\t[#ffc42a]'x0000O:    [#e9512b].:oooooool;.  [#0c8cd7].,::::::;'.
\t[#ffc42a]'xO00OO:  [#e9512b].;loooooo:,.  [#0c8cd7].';::;::;'.
\t[#ff9d20]'xOOOOOc[#ba1d49].'cllllllc'    [#0c83c8].,;;;;;;,.
\t[#ff9d20]'xOOOOOo[#ba1d49]:clllllc'.     [#0c83c8]';;;;;;'.
\t[#ff9d20]'xOOOOOd[#ba1d49]ccccc:,.       [#1a4ea4].',,,,'''.
\t[#ff9d20]'dOOOOkd[#ba1d49]c:::,.           [#1a4ea4]..''''''..
\t[#f68d1f]'dkkkkko[#ba1d49]:;,.               [#1a4ea4].''''','..
\t[#f68d1f]'dkkkkkl[#ba1d49],.                   [#0866b4].''',,,'.
\t[#f68d1f].lkkkkx;[#ba1d49].                     [#0866b4]..',,,,.
\t[#f68d1f] .;cc:'                         [#0866b4].....
 """
    console.print(txt)


@cli.command()
def change_passkey():
    """Change your encryption/decryption passkey"""
    YO9322()
    sys.exit()


@cli.command()
@click.option(
    "--file", hide_input=False, help="File to encrypt", prompt=True, required=True
)
def encrypt(file):
    """Encrypts .txt, .yaml, .json, & .csv files"""
    if file:
        JH0847(file)
        sys.exit()


@cli.command()
@click.option(
    "--file", hide_input=False, help="File to encrypt", prompt=True, required=True
)
def decrypt(file):
    """Decrypts .txt, .yaml, .json, & .csv files"""
    if file:
        IOA21H98(file)
        sys.exit()


# Log into RegScale to get a token
@cli.command()
@click.option(
    "--username",
    hide_input=False,
    help="RegScale User Name",
    prompt=True,
    required=True,
    default=lambda: os.environ.get("REGSCALE_USER", ""),
)
@click.option("--password", prompt=True, hide_input=True)
def login(username, password):
    """Logs the user into their RegScale instance"""
    if password:
        lg.login(username, password, app=app)
        sys.exit(0)


@cli.command()
def validate_token():
    """Check to see if token is valid"""
    if lg.is_valid(app=app):
        sys.exit(0)
    else:
        logger.warning("RegScale token is invalid, please login.")


# Check the health of the RegScale Application
@cli.command()
def healthcheck():
    """Monitoring tool to check the health of the RegScale instance"""
    hc.status()


# add Azure Active Directory (AD) support
cli.add_command(ad)

# add CISA support
cli.add_command(cisa)

# add Comparison support
cli.add_command(compare)

# add Microsoft Defender Recommendations Functionality
cli.add_command(defender)

# add Evidence support
cli.add_command(evidence)

# add JIRA support
cli.add_command(jira)

# add data migration support
cli.add_command(migrations)

# add OSCAL support
cli.add_command(oscal)

# add Reminder Functionality
cli.add_command(reminder)

# add ServiceNow support
cli.add_command(servicenow)

# add Tenable support
cli.add_command(tenable)

# add Wiz support
cli.add_command(wiz)

# start function for the CLI
if __name__ == "__main__":
    cli()
