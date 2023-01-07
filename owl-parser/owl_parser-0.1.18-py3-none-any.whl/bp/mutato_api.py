#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Mutato API """


from baseblock import BaseObject, Enforcer, Stopwatch

from owl_finder.multiquery.bp import FindOntologyData
from owl_parser.svc import (
    AugmentTokenHierarchy, PerformExactMatching, PerformHierarchyMatching,
    PerformSpanMatching)


class MutatoAPI(BaseObject):
    """ Mutato API """

    def __init__(self,
                 find_ontology_data: FindOntologyData):
        """ Change Log

        Created:
            6-Oct-2021
            craigtrim@gmail.com
            *   GRAFFL-CORE-0004
        Updated:
            1-Feb-2022
            craigtrim@gmail.com
            *   a finder initialization is a contract
                GRAFFL-CORE-0135
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
        Updated:
            28-Nov-2022
            craigtrim@gmail.com
            *   check if Ontology data actually exists
                https://github.com/craigtrim/owl-finder/issues/5

        Args:
            find_ontology_data (FindOntologyData): an instantiation of this object
        """
        BaseObject.__init__(self, __name__)
        if not find_ontology_data.lookup():
            raise ValueError('Empty Ontology')

        self._finder = find_ontology_data

        self._perform_exact_matching = PerformExactMatching(
            find_ontology_data).process

        self._perform_span_matching = PerformSpanMatching(
            find_ontology_data).process

        self._perform_hierarchal_matching = PerformHierarchyMatching(
            find_ontology_data).process

        self._augment_hierarchy = AugmentTokenHierarchy(
            find_ontology_data).process

        # ----------------------------------------------------------
        # Change Log:
        # 20220214  Disable Environment Check
        # 20220228  GRAFFL-CORE-0205
        # self._perform_spacy_matching = PerformSpacyMatching(
        #     find_ontology_data).process
        # ----------------------------------------------------------

    def swap(self,
             tokens: list,
             ctr: int = 0) -> list:

        sw = Stopwatch()

        if self.isEnabledForDebug:
            Enforcer.is_list_of_dicts(tokens)
            Enforcer.is_int(ctr)

        # ----------------------------------------------------------
        # Document:   Tokens vs Swaps
        # Reference:  GRAFFL-CORE-0074
        # ----------------------------------------------------------
        swaps = self._augment_hierarchy(tokens)
        swaps = self._perform_exact_matching(swaps)

        # ----------------------------------------------------------
        # Change Log:
        # 20221129  OWL-FINDER-0005  It is possible that spans may not exist
        # ----------------------------------------------------------
        if self._finder.spans() and len(self._finder.spans()):
            swaps = self._perform_span_matching(swaps)

        swaps = self._perform_hierarchal_matching(swaps)

        if ctr < 2:
            swaps = self.swap(swaps, ctr + 1)

        # ----------------------------------------------------------
        # Change Log:
        # 20220214  Disable Environment Check
        # 20220228  GRAFFL-CORE-0205
        # if EnvIO.exists_as_true('ENABLE_SPACY_SPANNING'):
        #   swaps = self._perform_spacy_matching(swaps)
        # ----------------------------------------------------------

        self.logger.info('\n'.join([
            'Synonym Swap Completed',
            f'\tTotal Time: {str(sw)}']))

        return swaps
