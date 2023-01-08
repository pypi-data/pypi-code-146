"""Console script for fhs_anki_ctrl."""
import sys

import typer

from pprint import pprint

from pathlib import Path
from typing import List

main = typer.Typer()

@main.command()
def dont_run(
        args_default: str = typer.Argument(..., help="Extra help")
):
    """Console script for fhs_anki_ctrl."""
    print(
        "Replace this message by putting your code into "
        "fhs_anki_ctrl.cli.ryb"
    )
    typer.secho(f"Some text!", fg = typer.colors.WHITE, bg = typer.colors.RED)

    import time
    with typer.progressbar(["1", "2", "3"]) as progress:
        for test in progress:
             time.sleep(1)
    return 0


@main.command()
def add_card(
        deck: str = typer.Option(..., help="Anki Deck to add cards to", envvar="anki_deck", prompt=True),
        question: str = typer.Option(..., help="the question to add", prompt=True),
        answer: str = typer.Option(..., help="the answer", prompt=True),
        debug: bool = typer.Option(False, "--debug", "-d", help="Debug mode"),
        config_file: str = typer.Option("", help="Config file to load."),
):
    """Add card."""
    from .config import config_read
    from .anki_class import AnkiClass
    config = config_read(config_file)
    anki = AnkiClass(config_dict=config, debug=debug)
    result = anki.add_card(deck=deck, question=question, answer=answer)
    pprint(result)


@main.command()
def add_qa_file(
        qa_file: List[Path] = typer.Argument(..., help="Text(s) file to process."),
        deck: str = typer.Option(..., help="Anki Deck to add cards to", envvar="anki_deck", prompt=True),
        dryrun: bool = typer.Option(False, "--dryrun", "-d", help="Dryrun mode"),
        sync: bool = typer.Option(False, "--sync", "-d", help="Sync to ankiweb after."),
        config_file: str = typer.Option("", help="Config file to load."),
):
    """Add card."""
    from .config import config_read
    from .anki_class import AnkiClass
    from .qa_file import load_qa_file
    config = config_read(config_file)
    anki = AnkiClass(config_dict=config)
    for path in qa_file:
        print(f"processing file: {path.name}")
        questions = load_qa_file(path)
        if dryrun is True:
            pprint(questions)
        else:
            result = anki.add_card_list(deck=deck, questions=questions)
            pprint(result)

    if sync is True and dryrun is False:
        print('sync.')
        result = anki.push_sync()
        pprint(result)



@main.command()
def sync(
        config_file: str = typer.Option("", help="Config file to load."),
):
    """Sync."""
    from .config import config_read
    from .anki_class import AnkiClass
    config = config_read(config_file)
    anki = AnkiClass(config_dict=config)
    result = anki.push_sync()
    pprint(result)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
