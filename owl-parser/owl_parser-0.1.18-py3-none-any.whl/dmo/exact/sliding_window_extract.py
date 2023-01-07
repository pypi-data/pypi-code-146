#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract Tokens using a Sliding Window Algorithm """


from pprint import pformat
from pprint import pprint

from baseblock import BaseObject, Stopwatch


class SlidingWindowExtract(BaseObject):
    """ Extract Tokens using a Sliding Window Algorithm """

    def __init__(self,
                 tokens: list,
                 gram_size: int):
        """
        Created:
            6-Oct-2021
            craigtrim@gmail.com
            *   GRAFFL-CORE-0004
        """
        BaseObject.__init__(self, __name__)
        self._tokens = tokens
        self._gram_size = gram_size

    def _process(self) -> list:
        results = []
        tokens = self._tokens

        if self._gram_size == len(tokens):
            return [tokens]

        if self._gram_size == 1:
            return [[x] for x in tokens]

        x = 0
        y = x + self._gram_size

        while y <= len(tokens):
            results.append(tokens[x: y])

            x += 1
            y = x + self._gram_size

        return results

    def process(self) -> list:
        sw = Stopwatch()

        results = self._process()

        # if self._gram_size == 2:
        #     print('Gram Size Extract 2')
        #     pprint(results)

        if self.isEnabledForDebug:

            self.logger.debug('\n'.join([
                'Sliding Window Extract Completed',
                f'\tGram Size: {self._gram_size}',
                f'\tTotal Tokens: {len(results)}',
                f'\tTotal Time: {str(sw)}']))

            if self._tokens != results:
                self.logger.debug('\n'.join([
                    'Sliding Window Extract Results',
                    f'\tTokens: {pformat(results, indent=4)}']))

        return results
