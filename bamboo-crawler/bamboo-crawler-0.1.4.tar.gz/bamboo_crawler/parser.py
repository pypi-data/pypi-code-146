from typing import Any, Dict, TextIO

import jinja2
from yaml.loader import Loader

Recipe = Any


def parse_ordered_yaml(infile: str) -> Recipe:
    loader = Loader(infile)
    try:
        return loader.get_single_data()
    finally:
        loader.dispose()  # type: ignore


def parse_recipe(infile: TextIO, config: Dict[str, Any]) -> Recipe:
    source = infile.read()
    template = jinja2.Template(source)
    rendered_source = template.render(**config)
    recipe = parse_ordered_yaml(rendered_source)
    return recipe
