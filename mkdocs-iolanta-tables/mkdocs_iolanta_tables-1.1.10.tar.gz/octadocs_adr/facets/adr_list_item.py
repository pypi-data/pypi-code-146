import functools
import operator
from pathlib import Path

import funcy
from dominate.tags import a, code, div, h1, h2, p
from dominate.util import raw

from iolanta.facet import Facet
from iolanta.renderer import render
from octadocs_adr.models import ADR


class ListItem(Facet):
    """ADR List item."""

    def html(self):
        row = self.query(
            (Path(__file__).parent / 'sparql/list_item.sparql').read_text(),
            adr_page=self.iri,
        ).first

        return div(
            h2(
                a(
                    code(
                        'ADR{:03d}'.format(row['number'].value),
                    ),
                    ' ',
                    row['title'],
                    href=row['url'],
                ),
            ),
            p(
                raw(
                    row.get('description', ''),
                ),
            ),
        )
