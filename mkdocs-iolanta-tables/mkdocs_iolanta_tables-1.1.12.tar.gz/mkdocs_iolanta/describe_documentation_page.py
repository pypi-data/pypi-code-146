from pathlib import Path
from typing import Iterator

from rdflib import RDF as rdf
from rdflib import Literal, URIRef

from mkdocs_iolanta.types import LOCAL as local
from mkdocs_iolanta.types import MKDOCS as mkdocs
from mkdocs_iolanta.types import Triple


def describe_documentation_page(
    iri: URIRef,
    path: Path,
    docs_dir: Path,
) -> Iterator[Triple]:
    """Describe the file properties and hierarchy for the given page."""
    yield Triple(iri, mkdocs.fileName, Literal(path.name))

    try:
        relative_path = path.relative_to(docs_dir)
    except ValueError:
        return

    try:
        breadcrumbs = list(relative_path.parents)[:-1]
    except ValueError:
        return

    children = [relative_path, *breadcrumbs]
    parents = [*children[1:], None]

    child_per_parent = zip(children, parents)

    for child, parent in child_per_parent:
        child_iri = local.term(str(child or ''))
        parent_iri = local.term(str(parent or ''))

        yield Triple(parent_iri, rdf.type, mkdocs.Directory)
        yield Triple(child_iri, mkdocs.isChildOf, parent_iri)

        if parent:
            yield Triple(parent_iri, mkdocs.fileName, Literal(parent.name))

