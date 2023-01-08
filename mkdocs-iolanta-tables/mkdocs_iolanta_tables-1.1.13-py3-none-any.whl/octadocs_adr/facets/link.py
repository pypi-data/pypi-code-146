from dataclasses import dataclass

from documented import DocumentedError
from dominate.tags import a, code
from more_itertools import first
from rdflib.term import Node

from iolanta.facet import Facet
from octadocs_adr.models import ADRNumberInvalid


@dataclass
class ADRNotFound(DocumentedError):
    """
    ADR was not found.

    !!! error "ADR not found"
        The page specified as {self.iri} was not found on this site.

        - Perhaps this page does not exist,
        - or it is not an ADR?

        Please check existence of this page and whether it is correctly
        described as an ADR, for example, has the required `number` property.
    """

    iri: Node


class LinkToADR(Facet):
    """Link to an ADR document."""

    sparql = '''
    SELECT * WHERE {
        ?page
            mkdocs:url ?url ;
            mkdocs:title ?label ;
            adr:number ?number .

        OPTIONAL {
            ?page adr:status / mkdocs:symbol ?symbol .
        }
    } ORDER BY ?number LIMIT 1
    '''

    def html(self):
        """As an HTML link."""
        descriptions = self.query(
            self.sparql,
            page=self.iri,
        )

        try:
            location = first(descriptions)
        except ValueError as err:
            raise ADRNotFound(iri=self.iri) from err

        number = location['number'].value

        if not isinstance(number, int):
            raise ADRNumberInvalid(
                number=number,
                page=self.uriref,
            )

        readable_number = f'ADR{number:03}'

        if symbol := location.get('symbol'):
            readable_number = f'{symbol} {readable_number}'

        return a(
            code(readable_number),
            ' ',
            location['label'],
            href=location['url'],
        )
