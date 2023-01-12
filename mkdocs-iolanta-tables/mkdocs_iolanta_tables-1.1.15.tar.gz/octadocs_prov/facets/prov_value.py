from dominate.tags import a
from more_itertools import first

from iolanta.facet import Facet
from iolanta.renderer import render


class ProvEntity(Facet):
    """Render a node with prov:value defined."""

    def html(self):
        """Render value and link to it."""
        rows = self.query(
            '''
            SELECT * WHERE {
                $node prov:value ?value .

                OPTIONAL {
                    $node prov:wasDerivedFrom ?source .
                }

                OPTIONAL {
                    $node rdfs:comment ?comment .
                }
            }
            ''',
            node=self.iri,
        )

        try:
            row = first(rows)
        except ValueError as err:
            raise ValueError(
                f'No `prov:value` was found for the node: {self.uriref}.'
            ) from err

        kwargs = {}
        if comment := row.get('comment'):
            kwargs.update(title=comment)

        rendered_value = render(
            node=row['value'],
            iolanta=self.iolanta,
        )

        if row.get('source'):
            return a(
                rendered_value,
                href=row['source'],
                target='_blank',
                **kwargs,
            )

        return rendered_value
