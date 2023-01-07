from pathlib import Path

from iolanta.facet import Facet


class Number(Facet):
    """ADR List item."""

    def html(self):
        row = self.query(
            (Path(__file__).parent / 'sparql/number.sparql').read_text(),
            adr_page=self.iri,
        ).first

        return 'ADR{:03d}'.format(row['number'].value)
