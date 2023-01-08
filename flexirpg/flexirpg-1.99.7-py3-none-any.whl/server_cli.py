# FlexiRPG server command line interface.
#
# Copyright (C) 2020 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import argparse

import cmd2

import orpg.networking.mplay_server

class ServerCli(cmd2.Cmd):
    """FlexiRPG server command line interface."""

    def __init__(self):
        cmd2.Cmd.__init__(self)

        self.orpg_server = orpg.networking.mplay_server.mplay_server()

    def start(self):
        self.orpg_server.initServer()

    def stop(self):
        self.orpg_server.kill_server()

    players_parser = argparse.ArgumentParser()

    @cmd2.with_argparser(players_parser)
    def do_players(self, args):
        """List connected players."""
        self.orpg_server.player_list()

    kick_parser = argparse.ArgumentParser()
    kick_parser.add_argument("player_id", type=int, help="ID of player")

    @cmd2.with_argparser(kick_parser)
    def do_kick(self, args):
        """Kick player from server."""
        try:
            self.orpg_server.admin_kick(args.player_id, "Kicked by server administrator")
        except KeyError:
            print(f"Player '{args.player_id}' not connected.")


def run_server():
    c = ServerCli()
    c.start()
    ret = c.cmdloop()
    c.stop()
    return ret
