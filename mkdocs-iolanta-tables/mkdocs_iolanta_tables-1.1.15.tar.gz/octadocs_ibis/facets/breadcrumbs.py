from typing import Dict, Iterable, TypeVar

import funcy
from dominate.tags import i
from funcy import first
from urlpath import URL

from iolanta.facet import Facet
from iolanta.namespaces import IOLANTA
from iolanta.renderer import render
from mkdocs_iolanta.environment import iri_to_url

Something = TypeVar('Something')


def path_depth(row: Dict[str, str]) -> int:
    """Depth of path."""
    url = URL(iri_to_url(row['parent_directory_index']))
    return len(url.parts)


def but_first(iterable: Iterable[Something]) -> Iterable[Something]:
    """Skip the first item of an iterable and return the remaining."""
    try:
        next(iterable)
    except StopIteration:
        pass

    return iterable


class Breadcrumbs(Facet):
    breadcrumbs_query = '''
    SELECT ?parent_directory_index ?parent_directory_index_subject WHERE {
        $this mkdocs:subjectOf* ?this_page .

        ?this_page mkdocs:isChildOf* ?parent_directory .
        ?parent_directory mkdocs:isParentOf ?parent_directory_index .
        ?parent_directory_index a mkdocs:IndexPage .

        ?parent_directory_index_subject mkdocs:subjectOf ?parent_directory_index .

        FILTER( ?parent_directory_index != ?this_page )
    } ORDER BY ?parent_directory_index
    '''

    page_type_query = '''
    SELECT ?type WHERE {
        $this a ?type .
        ?type mkdocs:position ?position .
    } ORDER BY ?position
    '''

    def renderable_page_type(self):
        return first(
            self.query(
                self.page_type_query,
                this=self.uriref,
            ),
        )['type']

    def html(self):
        rows = self.query(
            self.breadcrumbs_query,
            this=self.uriref,
        )

        sorted_rows = sorted(
            rows,
            key=path_depth,
        )

        instances = but_first(
            funcy.pluck(
                'parent_directory_index_subject',
                sorted_rows,
            ),
        )

        rendered_links = [
            render(
                instance,
                iolanta=self.iolanta,
                environments=[IOLANTA.html],
            )
            for instance in instances
        ]

        breadcrumbs = ' › '.join(map(str, rendered_links))

        rendered_type = i(
            render(
                self.renderable_page_type(),
                iolanta=self.iolanta,
                environments=[IOLANTA.html],
            ),
        )

        return ' › '.join(
            filter(
                bool,
                map(
                    str,
                    [
                        breadcrumbs,
                        rendered_type,
                    ],
                ),
            ),
        )
