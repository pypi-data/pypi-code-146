#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Perform Exact Matching """


from pprint import pprint

from baseblock import EnvIO
from baseblock import BaseObject
from baseblock import Enforcer
from baseblock import Stopwatch

from owl_finder.multiquery.bp import FindOntologyData

from owl_parser.dmo import ExactMatchFinder
from owl_parser.dmo import ExactMatchSwapper
from owl_parser.dmo import SwapResultSummarizer


class PerformExactMatching(BaseObject):
    """ Perform Exact Matching """

    def __init__(self,
                 find_ontology_data: FindOntologyData):
        """ Change Log

        Created:
            20-Oct-2021
            craigtrim@gmail.com
            *   refactored out of 'mutato-api'
                GRAFFL-CORE-0077
        Updated:
            26-May-2022
            craigtrim@gmail.com
            *   treat 'ontologies' param as a list
                https://github.com/grafflr/deepnlu/issues/7
        Updated:
            27-May-2022
            craigtrim@gmail.com
            *   remove all params in place of 'find-ontology-data'
                https://github.com/grafflr/deepnlu/issues/13
        Updated:
            25-Nov-2022
            craigtrim@gmail.com
            *   modify how 'exact-match-swapper' is called
                https://github.com/craigtrim/owl-parser/issues/1
        Updated:
            29-Nov-2022
            craigtrim@gmail.com
            *   perform early return in loop
                https://github.com/craigtrim/owl-parser/issues/10#issuecomment-1331531086

        Args:
            find_ontology_data (FindOntologyData): an instantiation of this object
        """
        BaseObject.__init__(self, __name__)
        self._d_lookup = find_ontology_data.lookup()
        self._exact_match_swapper = ExactMatchSwapper(
            find_ontology_data).process

    def _process(self,
                 tokens: list) -> list:

        gram_size = EnvIO.int_or_default('OWL_PARSER_GRAMSIZE', 10)
        while gram_size > 0:

            exact_match_finder = ExactMatchFinder(
                gram_size=gram_size,
                d_lookup=self._d_lookup).process

            results = exact_match_finder(tokens)

            if not results:
                gram_size -= 1
                continue

            for exact_match in results:

                d_swap = self._exact_match_swapper(exact_match)
                ids = [x['id'] for x in d_swap['swaps']['tokens']]

                merged = []
                for token in tokens:
                    if token['id'] not in ids:
                        merged.append(token)
                    elif token['id'] == ids[0]:
                        merged.append(d_swap)

                # -----------------------------------------------------
                # Change Log:
                # 20221129  https://github.com/craigtrim/owl-parser/issues/10#issuecomment-1331531086
                #           Use Early Return
                # -----------------------------------------------------
                return self._process(merged)

        return tokens

    def process(self,
                tokens: list) -> list:

        if self.isEnabledForDebug:
            Enforcer.is_list(tokens)

        sw = Stopwatch()

        swaps = self._process(tokens)

        if self.isEnabledForInfo:

            summary = SwapResultSummarizer().process(swaps)
            self.logger.info('\n'.join([
                'Exact Swapping Completed',
                f'\tEntity Summary: {summary}',
                f'\tTotal Time: {str(sw)}']))

        return swaps
