#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract Keyterms from Input Text using Textacy """


from baseblock import BaseObject, Stopwatch, TextUtils
from pandas import DataFrame
from textblob import Word


class FilterKeyterms(BaseObject):
    """ Filter a DataFrame of KeyTerms """

    def __init__(self):
        """ Change Log

        Created:
            18-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildolw/issues/3
        Updated:
            8-Aug-2022
            craigtrim@gmail.com
            *   eliminate subsumed tokens
                https://github.com/craigtrim/buildolw/issues/9
        Updated:
            7-Sept-2022
            craigtrim@gmail.com
            *   eliminate subsumed tokens
                https://github.com/craigtrim/owl-builder/issues/1
        """
        BaseObject.__init__(self, __name__)

    def _process(self,
                 df: DataFrame) -> list:

        if df is None or not len(df):
            return None

        terms = [x.lower() for x in list(df['Term'].unique())]

        subsumed = TextUtils.find_subsumed_tokens(terms)
        terms = [x for x in terms if x not in subsumed]

        # sort by length
        terms = sorted(set(terms), key=len, reverse=True)

        discards = set()

        # discard plurals
        for t1 in terms:
            for t2 in [x for x in terms if x != t1]:
                if f"{t1}s" == t2:
                    discards.add(t2)
                elif f"{t2}s" == t1:
                    discards.add(t1)

        # discard bigrams found in trigrams
        for t1 in [x for x in terms if len(x.split()) == 2]:
            for t2 in [x for x in terms if len(x.split()) == 3]:
                if f"{t1} " in t2 or f" {t1}" in t2:
                    discards.add(t1)

        terms = [x.strip() for x in terms if x not in discards]

        # discard larger length if word similarity value is close
        for t1 in terms:
            for t2 in [x for x in terms if x != t1]:
                if TextUtils.jaccard_similarity(t1, t2) >= 0.85:
                    if len(t1) > len(t2):
                        discards.add(t1)
                    else:
                        discards.add(t2)

        # given a term like 'wi-fi' discard any 'wi' and 'fi' terms
        for tokens in [x.split('-') for x in terms if '-' in x]:
            [discards.add(x) for x in tokens if x in terms]

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                "Tokens Filtering Completed",
                f"\tTotal Discards: {len(discards)}",
                f"\t\t{list(discards)}"]))

        terms = [x.strip() for x in terms if x not in discards]

        def has_bad_char(a_term: str) -> str:
            if '(' in a_term:
                return True
            if ')' in a_term:
                return True
            return False

        terms = [x for x in terms if not has_bad_char(x)]

        # lemmatize individual tokens in each term
        lemmatized_terms = set()
        for term in terms:
            tokens = term.split()
            term = ' '.join([Word(x).lemmatize() for x in tokens]).strip()
            lemmatized_terms.add(term.strip())

        lemmatized_terms = [x.strip() for x in lemmatized_terms]
        return sorted(lemmatized_terms, key=len, reverse=True)

    def process(self,
                df: DataFrame) -> list:
        """ Filter Keyterms

        Args:
            df (DataFrame): incoming pandas dataframe
            Sample Input:
                +----+----------+--------+------------+-----------------+
                |    | Term     |   Size |      Score | Source          |
                |----+----------+--------+------------+-----------------|
                |  0 | meeting  |      1 |   0.134722 | kt.textrank     |
                |  1 | tomorrow |      1 |   0.080897 | kt.textrank     |
                |  2 | pm       |      1 |   0.080897 | kt.textrank     |
                ...
                | 21 | 1 pm     |      2 | nan        | terms.3         |
                +----+----------+--------+------------+-----------------+

        Returns:
            list: the filtered results
        """

        sw = Stopwatch()

        results = self._process(df)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Keyword Filtering Complete",
                f"\tTotal Time: {str(sw)}",
                f"\tTotal Size: {len(df)}"]))

        return results
