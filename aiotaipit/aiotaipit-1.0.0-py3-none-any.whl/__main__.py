"""Provide a CLI for Taipit."""
import asyncio

from aiotaipit.cli import cli

if __name__ == "__main__":
    asyncio.run(cli())
