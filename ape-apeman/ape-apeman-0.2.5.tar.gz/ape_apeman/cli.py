# cli for ape-apeman

import sys

import click
from box import Box
from eth_utils import from_wei, to_checksum_address

from .context import APE
from .exception_handler import ExceptionHandler
from .json import dumps
from .version import __timestamp__, __version__

header = f"{__name__.split('.')[0]} v{__version__} {__timestamp__}"


def output(ctx, data):
    if ctx.obj.json:
        kwargs = dict(humanize=ctx.obj.humanize, hex_bytes=True)
        if ctx.obj.compact:
            kwargs["separators"] = (",", ":")
        else:
            kwargs["indent"] = 2
        data = dumps(data, **kwargs)
    click.echo(data)


def fail(message):
    click.echo(f"Failed: {message}", err=True)
    sys.exit(1)


@click.group(name="apeman")
@click.version_option(message=header)
@click.option(
    "-e",
    "--ecosystem",
    type=str,
    required=True,
    envvar="APE_ECOSYSTEM",
    show_envvar=True,
    default="ethereum",
)
@click.option(
    "-n",
    "--network",
    type=str,
    required=True,
    envvar="APE_NETWORK",
    show_envvar=True,
)
@click.option(
    "-p",
    "--provider",
    type=str,
    required=True,
    envvar="APE_PROVIDER",
    show_envvar=True,
)
@click.option("-d", "--debug", is_flag=True, help="debug mode")
@click.option(
    "-j/-r",
    "--json/--raw",
    is_flag=True,
    default=True,
    help="select output format",
)
@click.option("-c", "--compact", is_flag=True, help="output compact json")
@click.option(
    "-h", "--humanize", is_flag=True, help="human-friendly (but lossy) output"
)
@click.pass_context
def cli(ctx, ecosystem, network, debug, provider, json, compact, humanize):
    ctx.obj = Box(ehandler=ExceptionHandler(debug))
    ctx.obj.debug = debug
    ctx.obj.json = json
    ctx.obj.compact = compact
    ctx.obj.humanize = humanize
    ctx.obj.ape = APE(ecosystem, network, provider)


@cli.command
@click.option("-u", "--url", is_flag=True, help="output transaction url")
@click.option(
    "-l", "--logs", is_flag=True, help="output decoded transaction logs"
)
@click.argument("txn-hash", type=str)
@click.pass_context
def txn(ctx, url, logs, txn_hash):
    """output transaction receipt"""
    with ctx.obj.ape as ape:
        if url:
            ret = ape.explorer.get_transaction_url(txn_hash)
        elif logs:
            receipt = ape.provider.get_receipt(txn_hash)
            logs = receipt.decode_logs()
            ret = [log.dict() for log in logs]
        else:
            receipt = ape.provider.get_receipt(txn_hash)
            ret = receipt.dict()

    output(ctx, ret)


@cli.command
@click.argument("account", type=str)
@click.option("-w", "--wei", is_flag=True, help="output wei")
@click.option("-g", "--gwei", is_flag=True, help="output gwei")
@click.option("-e", "--ether", is_flag=True, help="output ether")
@click.pass_context
def balance(ctx, account, wei, gwei, ether):
    """output account balance"""
    account = to_checksum_address(account)
    with ctx.obj.ape as ape:
        as_wei = ape.provider.get_balance(account)
    as_ether = from_wei(as_wei, "ether")
    as_gwei = from_wei(as_wei, "gwei")
    if wei:
        ret = as_wei
    elif gwei:
        ret = as_gwei
    elif ether:
        ret = as_ether
    else:
        ret = {account: dict(wei=as_wei, gwei=as_gwei, ether=as_ether)}

    output(ctx, ret)


@cli.group
@click.pass_context
def eth(ctx):
    """expose web3.eth methods"""
    pass


@eth.command
@click.pass_context
def get_block_number(ctx):
    with ctx.obj.ape as ape:
        ret = ape.web3.eth.get_block_number()
    output(ctx, ret)


@eth.command
@click.argument("block", type=str)
@click.pass_context
def get_block(ctx, block):
    if block.isnumeric():
        block = int(block)
    with ctx.obj.ape as ape:
        _block = ape.web3.eth.get_block(block)
        ret = dict(_block)
    output(ctx, ret)


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
