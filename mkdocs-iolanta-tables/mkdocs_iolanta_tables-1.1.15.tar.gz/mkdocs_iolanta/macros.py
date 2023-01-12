from functools import partial
from typing import List, Optional, Union

from mkdocs_macros.plugin import MacrosPlugin
from rdflib import URIRef

from iolanta.iolanta import Iolanta
from iolanta.renderer import render
from mkdocs_iolanta.types import LOCAL

Environments = Union[str, List[str]]


def macro_render(
    thing: Union[str, URIRef],
    iolanta: Iolanta,
    environments: Optional[Environments] = None,
):
    """Macro to render something with Iolanta."""
    if ':' not in thing:
        thing = f'local:{thing}'

    thing = iolanta.graph.namespace_manager.expand_curie(thing) or thing

    if isinstance(environments, str):
        environments = [environments]

    elif environments is None:
        environments = []

    environments = [
        URIRef(f'local:{environment}') if (
            isinstance(environment, str)
            and ':' not in environment
        ) else environment
        for environment in environments
    ]

    return render(
        node=URIRef(thing),
        iolanta=iolanta,
        environments=[URIRef(environment) for environment in environments],
    )


def define_env(env: MacrosPlugin) -> MacrosPlugin:  # noqa: WPS213
    """Create mkdocs-macros Jinja environment."""
    env.variables['LOCAL'] = LOCAL
    env.variables['local'] = LOCAL

    iolanta = env.variables.iolanta

    env.macro(
        partial(
            macro_render,
            iolanta=iolanta,
        ),
        name='render',
    )

    return env
