from typing import List

from click.core import Argument, Context

from clutchGen.configs import get_all_template_name


def complete_templates_names(_: Context, __: Argument, incomplete: str) -> List[str]:
    all_names = get_all_template_name()
    return [name for name in all_names if name.startswith(incomplete)] if incomplete else all_names
