# SPDX-License-Identifier: MIT
# Copyright (c) 2023 David Lechner <david@lechnology.com>

import argparse
import curses
import enum
import re
import sys

from chess import pgn

from . import __version__ as package_version

if sys.platform == "win32":
    from .winsdk_helper import speak
elif sys.platform == "darwin":
    from .pyobjc_helper import speak
else:
    print(f"unsupported platform: '{sys.platform}'", file=sys.stderr)
    exit(1)


class Key(enum.IntEnum):
    B = ord("b")
    C = ord("c")
    F = ord("f")
    L = ord("l")
    N = ord("n")
    P = ord("p")
    Q = ord("q")
    R = ord("r")


PIECE = {
    "R": "rook",
    "B": "bishop",
    "N": "knight",
    "Q": "queen",
    "K": "king",
    "O-O": "castles kingside",
    "O-O-O": "castles queenside",
}

PROMOTION = {
    "=N": "promotes to knight",
    "=B": "promotes to bishop",
    "=R": "promotes to rook",
    "=Q": "promotes to queen",
}

CHECK = {
    "+": "check",
    "#": "checkmate",
}

RESULT = {
    "1/2-1/2": "ended in a draw",
    "1-0": "white won",
    "0-1": "black won",
    "*": "game continued",
}

NAG = {
    pgn.NAG_GOOD_MOVE: "good move.",
    pgn.NAG_MISTAKE: "mistake.",
    pgn.NAG_BRILLIANT_MOVE: "brilliant move.",
    pgn.NAG_BLUNDER: "blunder.",
    pgn.NAG_SPECULATIVE_MOVE: "speculative move.",
    pgn.NAG_DUBIOUS_MOVE: "dubious move.",
}


def expand(move: str) -> str:
    """
    Expands a chess move.

    The piece name is spelled out as are check/checkmate symbols.

    Args:
        move: A chess move in standard algebraic notation.

    Returns:
        The move expanded so that is suitable for a text-to-speech engine.
    """

    match = re.match(
        r"^([RNBQK]|O-O(?:-O)?)?([a-h]?[1-8]?)??(x)?([a-h][1-8])?(=[BNRQ])?([+#])?$",
        move,
    )

    piece, start, captures, end, promotion, check = match.groups()
    segments = list[str]()

    if piece:
        segments.append(PIECE[piece])

    if start:
        segments.append(" ".join(start))

    if captures:
        segments.append("takes")

    if end:
        segments.append(" ".join(end))

    if promotion:
        segments.append(PROMOTION[promotion])

    if check:
        segments.append(CHECK[check])

    return " ".join(segments)


def fixup_comment(comment: str) -> str:

    return (
        re.sub(r"\[[^\]]*\]", "", comment)
        .replace(" $1", "!")
        .replace(" $2", "?")
        .replace("\n", " ")
    )


def app(stdscr: curses.window, game: pgn.Game):
    stdscr.addstr("PGN Speaker\n")
    stdscr.addstr("-----------\n")
    stdscr.addstr("commands: (n)ext, (b)ack, (r)epeat, (f)irst, (l)ast, (q)uit\n")
    stdscr.addstr("\n")

    x, y = stdscr.getyx()

    node = game

    while True:
        key = stdscr.getch()

        match key:
            case Key.Q:
                # quit program
                break
            case Key.N | curses.KEY_RIGHT:
                # next move
                if node is not None:
                    # if we are not at the end of the file already go to the next move
                    node = node.next()
            case Key.B | curses.KEY_LEFT:
                # back one move
                if node is None:
                    # if we are at the end of the file, go to the last move
                    node = game.end()
                else:
                    # go to the previous move
                    node = node.parent

                    if node is None:
                        # we are at the start of the file
                        node = game
            case Key.R:
                # repeat - don't change node
                pass
            case Key.F | curses.KEY_UP:
                # first move
                node = game.next()
            case Key.L | curses.KEY_DOWN:
                # last move
                node = game.end()
            case Key.C:
                # comment
                comments = list[str]()

                if node is not None:
                    comments.extend(NAG[nag] for nag in node.nags)

                    if node.comment:
                        comments.append(fixup_comment(node.comment))

                if comments:
                    speak(" ".join(comments))
                else:
                    speak("no comment")

                continue
            case _:
                # all other keys ignored
                continue

        stdscr.move(x, y)
        stdscr.clrtoeol()

        if node is None:
            # end of game
            result = game.headers["Result"]
            stdscr.addstr(result)
            speak(RESULT[result])
        elif node.parent is None:
            start = "start of game"
            stdscr.addstr(start)
            speak(start)
        else:
            move_num = (node.ply() + 1) // 2
            turn, color = ("...", "black") if node.turn() else (" ", "white")
            move = node.san()

            stdscr.addstr(f"{move_num}{turn}{move}")
            speak(f"{move_num} {color} {expand(move)}")


def main():
    parser = argparse.ArgumentParser("pgn-speaker")

    parser.add_argument(
        "file",
        metavar="<file>",
        type=argparse.FileType(),
        help="the path to a .pgn file",
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {package_version}"
    )

    args = parser.parse_args()

    game = pgn.read_game(args.file)

    curses.wrapper(app, game)
