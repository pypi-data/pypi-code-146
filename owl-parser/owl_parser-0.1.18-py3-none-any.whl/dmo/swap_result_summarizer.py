#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Summarize the Results of a Token Swap """


from typing import List

from pprint import pformat
from baseblock import BaseObject, Enforcer, Stopwatch

from owl_finder.multiquery.bp import FindOntologyData
from owl_parser.dmo import ExactMatchFinder, ExactMatchSwapper


class SwapResultSummarizer(BaseObject):
    """ Summarize the Results of a Token Swap """

    def __init__(self):
        """ Change Log

        Created:
            25-Nov-2022
            craigtrim@gmail.com
            *   created in pursuit of
                https://github.com/craigtrim/owl-parser/issues/1
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                results: List[dict]) -> List[str]:

        entities = []
        for result in results:

            t_result = type(result)

            if t_result == dict:
                entities.append(result['normal'])

            elif t_result == list:
                for item in result:

                    t_item = type(item)
                    if t_item == dict:
                        entities.append(item['normal'])
                    else:
                        raise TypeError(f'Unexpected Type-2: {t_item}')

            else:

                raise TypeError(f'Unexpected Type-2: {t_result}')

        return entities
