#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Orchestrate Taxonomy Generation """


from typing import List
from typing import Optional

from pandas import DataFrame

from baseblock import BaseObject
from baseblock import Enforcer

from owl_builder.autotaxo.svc import ExtractKeyterms
from owl_builder.autotaxo.svc import FilterKeyterms
from owl_builder.autotaxo.svc import GenerateTaxonomyDataFrame
from owl_builder.autotaxo.svc import GenerateTaxonomyTTL
from owl_builder.autotaxo.dto import load_model


class AutoTaxoOrchestrator(BaseObject):
    """ Orchestrate Taxonomy Generation """

    __model = None

    def __init__(self):
        """ Change Log:

        Created:
            16-Apr-2022
            craigtrim@gmail.com
            *   in pursuit of "Auto Taxonomy Building with Textacy Library #286"
        Updated:
            2-May-2022
            craigtrim@gmail.com
            *   renamed from 'generate-taxonomy'
        Updated:
            18-Jul-2022
            craigtrim@gmail.com
            *   overhaul end-to-end process
                https://github.com/craigtrim/buildolw/issues/3
        Updated:
            16-Aug-2022
            craigtrim@gmail.com
            *   assert return types per
                https://bast-ai.atlassian.net/browse/COR-94?focusedCommentId=10203
        Updated:
            19-Oct-2022
            craigtrim@gmail.com
            *   use lazy loading for model in pursuit of
                https://github.com/craigtrim/climate-mdl-builder/issues/5
        Updated:
            14-Dec-2022
            craigtrim@gmail.com
            *   deprecate 'ttlbuilder' and expose 'build_ttl'
                https://github.com/craigtrim/owl-builder/issues/2
        """
        BaseObject.__init__(self, __name__)

    def _model(self):
        if not self.__model:
            self.__model = load_model()
        return self.__model

    def keyterms(self,
                 input_text: str,
                 use_terms: bool = True,
                 use_keyterms: bool = True,
                 use_ngrams: bool = False,
                 use_nounchunks: bool = False) -> list or None:
        """ Generate KeyTerms as a simple list

        Args:
            input_text (str): input text of any length or description
            use_terms (bool, optional). Use Simple Term extraction algorithms. Default is True.
            use_keyterms (bool, optional). Use KeyTerm extraction algorithms. Default is True.
            use_ngrams (bool, optional). Use n-Gram extraction algorithms. Default is False.
            use_nounchunks (bool, optional). Use Noun Chunk extraction algorithms. Default is False.

        Sample Input:
            A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.
            By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.
            Ethernet and Wi-Fi are the two most common technologies in use for local area networks.
            Historical network technologies include ARCNET, Token Ring, and AppleTalk.

        Sample Output:
            [   'leased telecommunication circuit',
                'historical network technology',
                'large geographic distance',
                'interconnects computer',
                'local area network',
                'university campus',
                'common technology',
                'wide area network',
                'computer network',
                'office building',
                'include arcnet',
                'limited area',
                'token ring'
            ]

        Returns:
            list or None: list of keyterms
        """
        svc = ExtractKeyterms(self._model())

        if self.isEnabledForDebug:
            Enforcer.is_str(input_text)

        df_keyterms = svc.process(input_text,
                                  use_terms=use_terms,
                                  use_keyterms=use_keyterms,
                                  use_ngrams=use_ngrams,
                                  use_nounchunks=use_nounchunks)

        if self.isEnabledForDebug:
            assert type(df_keyterms) == DataFrame

        keyterms = FilterKeyterms().process(df_keyterms)

        if self.isEnabledForDebug:
            Enforcer.is_optional_list(keyterms)

        return keyterms

    def dataframe(self,
                  input_text: str) -> DataFrame:
        """ Generate KeyTerms as a Pandas DataFrame

        Args:
            input_text (str): input text of any length or description

        Sample Input:
            A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.
            By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.
            Ethernet and Wi-Fi are the two most common technologies in use for local area networks.
            Historical network technologies include ARCNET, Token Ring, and AppleTalk.

        Sample Output:
            +----+---------------------------+----------------------------------+--------------+
            |    | Parent                    | Child                            | Confidence   |
            |----+---------------------------+----------------------------------+--------------|
            |  0 | circuit                   | telecommunication circuit        | e            |
            |  1 | telecommunication circuit | leased telecommunication circuit | e            |
            |  2 | technology                | network technology               | i            |
            |  3 | network technology        | historical network technology    | i            |
            |  4 | distance                  | geographic distance              | a            |
            |  5 | geographic distance       | large geographic distance        | a            |
            |  6 | computer                  | interconnects computer           | n            |
            |  7 | network                   | area network                     | o            |
            |  8 | area network              | local area network               | o            |
            |  9 | network                   | area network                     | i            |
            | 10 | area network              | wide area network                | i            |
            | 11 | technology                | common technology                | o            |
            | 12 | campus                    | university campus                | n            |
            | 13 | network                   | computer network                 | o            |
            | 14 | building                  | office building                  | f            |
            | 15 | arcnet                    | include arcnet                   | n            |
            | 16 | area                      | limited area                     | i            |
            | 17 | ring                      | token ring                       | o            |
            +----+---------------------------+----------------------------------+--------------+
        Returns:
            DataFrame: list of keyterms
        """

        keyterms = self.keyterms(input_text)
        return GenerateTaxonomyDataFrame().process(keyterms)

    def build_ttl(self,
                  input: str or DataFrame) -> Optional[List[str]]:
        """ Generate TTL Results for augmenatation of OWL model

        Args:
            input (str or DataFrame): either input text or a DataFrame

                input_text:  any input text string of any length
                    Purpose:
                        If the consumer is sending plain-text input it means they want this microservice to create the taxonomy
                        prior to generate the TTL code
                    Sample Input:
                        A local area network (LAN) is a computer network that interconnects computers within a limited area.

                DataFrame: a Dataframe with Parent/Child taxonomy columns.
                    Purpose:
                        If the consumer is sending a Datafraame of this format, it means they want the TTL generator to use
                        their own taxonomy, rather than creating one on-the-fly
                    Sample Input:
                        +----+---------------------------+----------------------------------+
                        |    | Parent                    | Child                            |
                        |----+---------------------------+----------------------------------+
                        |  0 | circuit                   | telecommunication circuit        |
                        |  1 | telecommunication circuit | leased telecommunication circuit |
                        |  2 | technology                | network technology               |
                        +----+---------------------------+----------------------------------+

        Returns:
            Optional[List[str]]: TTL results for OWL model
                Sample Output:
                    ###  http://graffl.ai/pathology#telecommunication_circuit
                                :telecommunication_circuit rdf:type owl:Class ;
                                rdfs:label "Telecommunication Circuit" ;
                                rdfs:subClassOf :circuit .
                    ###  http://graffl.ai/pathology#circuit
                                :circuit rdf:type owl:Class ;
                                rdfs:label "Circuit" .
                    ###  http://graffl.ai/pathology#leased_telecommunication_circuit
                                :leased_telecommunication_circuit rdf:type owl:Class ;
                                rdfs:label "Leased Telecommunication Circuit" ;
                                rdfs:subClassOf :telecommunication_circuit .
                    ...
                    ###  http://graffl.ai/pathology#token_ring
                                :token_ring rdf:type owl:Class ;
                                rdfs:label "Token Ring" ;
                                rdfs:subClassOf :ring .
                    ###  http://graffl.ai/pathology#ring
                                :ring rdf:type owl:Class ;
                                rdfs:label "Ring" .
        """

        def get_taxonomy_df() -> DataFrame:
            type_input = type(input)
            if type_input == str:
                return self.dataframe(input)
            elif type(input) == DataFrame:
                if not set(['Parent', 'Child']).issubset(set(input.columns)):
                    raise ValueError("Unexpected DataFrame")
                return input
            raise TypeError(type_input)

        ttl_generator = GenerateTaxonomyTTL().process
        return ttl_generator(get_taxonomy_df())

    # TODO: Deprecated on 14-DEC-2022
    def ttlresults(self, input_text: str) -> list or None:
        self.logger.warn(
            "\n\n!!!This Method is Deprecated -- use 'build_ttl' instead\n\n!!!")
        df_taxo = self.dataframe(input_text)
        return GenerateTaxonomyTTL().process(df_taxo)
