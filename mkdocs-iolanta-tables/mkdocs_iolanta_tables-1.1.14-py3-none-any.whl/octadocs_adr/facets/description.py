from pathlib import Path

from dominate.tags import div, p
from dominate.util import raw

from iolanta.facet import Facet

TEMPLATE = '''
!!! note "TL;DR"
    {}

<div class="admonition note">
<p class="admonition-title">TL;DR</p>
<p>boo</p>
</div>
'''


class Description(Facet):
    """ADR Description."""

    def html(self):
        row = self.query(
            (Path(__file__).parent / 'sparql/description.sparql').read_text(),
            adr_page=self.iri,
        ).first

        return div(
            p(
                'TL;DR',
                cls='admonition-title',
            ),
            p(
                raw(row['description']),
            ),
            cls='admonition note',
        ) if row else ''
