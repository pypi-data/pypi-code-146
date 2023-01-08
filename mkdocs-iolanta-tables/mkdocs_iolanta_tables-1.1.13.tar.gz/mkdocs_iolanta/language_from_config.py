from typing import Optional

from mkdocs.theme import Theme


def language_from_config(config) -> Optional[str]:
    """Retrieve language from config."""
    theme: Theme = config['theme']
    return theme['language']

