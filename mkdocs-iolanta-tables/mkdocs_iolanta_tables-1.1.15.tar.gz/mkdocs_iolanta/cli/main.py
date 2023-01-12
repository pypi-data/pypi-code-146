from mkdocs.config import load_config
from more_itertools import consume
from typer import Typer

from mkdocs_iolanta.cli import context, show, sparql


def generate_app() -> Typer:
    app = Typer()

    app.add_typer(sparql.app)
    app.add_typer(context.app)
    app.add_typer(show.app)

    config = load_config()

    typer_instances = [
        plugin.typer()
        for plugin in config['plugins'].values()
        if hasattr(plugin, 'typer')
    ]

    typer_instances = filter(bool, typer_instances)

    consume(
        map(
            app.add_typer,
            typer_instances,
        ),
    )

    return app


app = generate_app()
