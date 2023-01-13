from . import rules
from spacy import load, Language
import re


class CommaCorrector:
    """
    Corrects punctuation in given sentences.
    """

    def __init__(self, sentences: list[str] = []) -> None:
        self._nlp: Language = load("pl_core_news_sm")

        self._sentences: list[str] = sentences
        self._sentences_docs: list[Language] = self.create_docs(
            self._sentences)

        # get all rules from rules.py
        self._rules: dict = {rule[6:]: getattr(rules, rule) for rule in dir(
            rules) if rule.startswith('check_')}

        # get all keys from rules dict
        self._rules_keys: list[str] = [key for key in self._rules.keys()]

    def create_docs(self, sentences: list[str]) -> list[Language]:
        """Creates spaCy documents from given sentences."""
        return self._nlp.pipe(sentences)

    @staticmethod
    def _join_sentence(sentence: list[str]) -> str:
        """Joins list of words into sentence. Removes spaces before punctuation marks."""
        sentence = ' '.join(sentence)

        sentence = re.sub(r' ([.,?!:;])', r'\1', sentence)

        return sentence

    def _correct_sentence(self, sentence_doc) -> str:
        """
        Corrects punctuation in given sentence.

        Returns:
            str: Corrected sentence.
        """

        # transform spaCy document into list of words
        sentence_text: list[str] = [
            token.text for token in sentence_doc]

        # shift is used to correct index of token in sentence, if comma was inserted
        shift: int = 0

        # occured is used to check if rule was already used. Used to check for enumeration.
        occured: dict[str, bool] = {key: False for key in self._rules_keys}

        # iterate over all tokens in sentence
        for token in sentence_doc:
            index = token.i

            # skip first token, because it will never have a comma before it
            if index == 0:
                continue

            # skip if token is not in rules, because it is (probably) not a word, that can have comma before it
            if token.text not in self._rules_keys:
                continue

            # get result of rule check in format {'insert': bool, 'insert_pos': int, 'occured': bool}
            result = self._rules[token.text](
                token, sentence_doc[index - 1], occured[token.text])

            # set occured to True, if rule was used and it's possible to be an enumeration
            occured[token.text] = result['occured']

            # skip if comma should not be inserted
            if not result['insert']:
                continue

            # check if token at position index + result['insert_pos'] is not a punctuation mark
            if sentence_text[index + result['insert_pos'] + shift - 1] == ',':
                continue

            # insert comma result['insert_pos'] characters before token
            sentence_text.insert(index + result['insert_pos'], ',')

            # increase shift by 1, because comma was inserted
            shift += 1

        return self._join_sentence(sentence_text)

    def correct(self, sentences: list[str] = []) -> list[str]:
        """Corrects punctuation in all sentences."""

        if sentences == []:
            raise ValueError('Sentences list is empty.')
        
        self._sentences = sentences
        self._sentences_docs = self.create_docs(self._sentences)

        return [self._correct_sentence(sentence_doc) for sentence_doc in self._sentences_docs]
