#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Augment Tokens with Descendant and Ancestory Hierarchy for Inference Purposes """


from baseblock import BaseObject, Enforcer, Stopwatch

from owl_finder.multiquery.bp import FindOntologyData


class AugmentTokenHierarchy(BaseObject):
    """ Augment Tokens with Descendant and Ancestory Hierarchy for Inference Purposes """

    def __init__(self,
                 find_ontology_data: FindOntologyData):
        """ Change Log

        Created:
            14-Feb-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/188
        Updated:
            26-May-2022
            craigtrim@gmail.com
            *   remove 'ontology_name' as a param in pursuit of
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
        self._find_ancestors = find_ontology_data.ancestors
        self._find_descendants = find_ontology_data.descendants

    def _process(self, tokens: list) -> list:

        d_normals = {token['normal']: []
                     for token in tokens
                     if token['normal'].isalpha()}

        for normal in d_normals:
            d_normals[normal].append(self._find_ancestors(normal))
            d_normals[normal].append(self._find_descendants(normal))

        for token in tokens:
            if token['normal'] not in d_normals:
                continue

            values = d_normals[token['normal']]
            token['ancestors'] = values[0]  # ancestor position
            token['descendants'] = values[1]  # descendant position

        return tokens

    def process(self,
                tokens: list) -> list:

        if self.isEnabledForDebug:
            Enforcer.is_list(tokens)

        sw = Stopwatch()

        tokens = self._process(tokens)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                'Hierarchy Augmentation Completed',
                f'\tTotal Time: {str(sw)}']))

        return tokens
