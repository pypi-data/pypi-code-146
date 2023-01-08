import re

from mkdocs_iolanta.types import LOCAL


def iri_to_url(iri: str) -> str:
    """Convert Zet IRI into clickable URL."""
    iri = iri.replace(str(LOCAL), '')

    if iri.endswith('index.md'):
        return re.sub(
            r'/index\.md$',
            '/',
            iri,
        )

    else:
        return re.sub(
            r'\.md$',
            '',
            iri,
        )
