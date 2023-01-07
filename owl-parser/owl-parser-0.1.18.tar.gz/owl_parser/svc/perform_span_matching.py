#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Perform Span Matching """


from baseblock import BaseObject, Enforcer, Stopwatch

from owl_finder.multiquery.bp import FindOntologyData
from owl_parser.dmo import SpanMatchFinder, SpanMatchSwapper


class PerformSpanMatching(BaseObject):
    """Perform Span Matching

    Sample Input:
        the history of nursing

    Sample Rule:
        nursing_history ~ nurse+history

    Sample Match:
        "history of nursing" == nursing_history

    Sample Output:
        the nursing_history
    """

    def __init__(self,
                 find_ontology_data: FindOntologyData):
        """ Change Log

        Created:
            20-Oct-2021
            craigtrim@gmail.com
            *   GRAFFL-CORE-0077
        Updated:
            26-May-2022
            craigtrim@gmail.com
            *   treat 'ontologies' param as a list
                https://github.com/grafflr/deepnlu/issues/7
        Updated:
            27-May-2022
            craigtrim@gmail.com
            *   remove 'ontologies' and integrate 'find-ontology-data'
                https://github.com/grafflr/deepnlu/issues/13

        Args:
            find_ontology_data (FindOntologyData): an instantiation of this object
        """
        BaseObject.__init__(self, __name__)
        self._span_match_finder = SpanMatchFinder(
            d_spans=find_ontology_data.spans(),
            span_keys=find_ontology_data.span_keys()).process
        self._span_match_swapper = SpanMatchSwapper(find_ontology_data)

    def _process(self,
                 tokens: list) -> list:

        matching_rules = self._span_match_finder(tokens)
        if not matching_rules or not len(matching_rules):
            return tokens

        tokens = self._span_match_swapper.process(
            tokens=tokens,
            matching_rules=matching_rules)

        return tokens

    def process(self,
                tokens: list) -> list:

        if self.isEnabledForInfo:
            sw = Stopwatch()
            Enforcer.is_list(tokens)

        swaps = self._process(tokens)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                'Span Swapping Completed',
                f'\tTotal Time: {str(sw)}']))

        return swaps
