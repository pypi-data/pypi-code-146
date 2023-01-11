"""
Utilities for dealing with natural languages. Included is a self-contained
tokenizer based on regular expressions and data generators for naive sentiment
analysis.
"""

import random
import re
from typing import List

import nltk
import pandas as pd

from truera.client.nn.wrappers import nlp

nltk.download('stopwords')
from nltk.corpus import stopwords

# Collections of synonyms for test data generation for toy sentiment models.
GOOD_SYNONYMS = ["good", "alright", "buena", "well", "nice", "decent", "best"]
BAD_SYNONYMS = [
    "bad", "mala", "naughty", "rotten", "amiss", "wicked", "negative",
    "unfavourable", "horrid"
]
NEUTRAL_SYNONYMS = [
    "neutral"
]  #, "neutrality"] # not including neutrality as the greedy tokenizer cannot handle it due to it having a prefix that is another token.
SYNONYMS = dict(good=GOOD_SYNONYMS, bad=BAD_SYNONYMS, neutral=NEUTRAL_SYNONYMS)


def remove_stop_words(language: str, tokens_set: set) -> list:
    '''
    Given a language and the list of tokens present in all the sentences of
    segments, remove the stop words (SW) and return the final list which doesn't
    have SW

    Args:
        - language (str): Language for which we need stop words. 
        - tokens_set (set): All the tokens present in both the segments
    Returns:
        - List: A list which has all the tokens except SW.
    '''
    stop_words = set(stopwords.words(language))
    segment_tokens_filtered_sw_removed = [
        w for w in tokens_set if not w.lower() in stop_words
    ]
    return segment_tokens_filtered_sw_removed


def generate_dataset_sharp(num_rows: int, row_length: int, seed=0xdeadbeef):
    """
    Generate random sentiment sentences and their labels. Uses only the tokens
    "good", "bad", "neutral", and their synonyms but also creates words that
    combine these tokens. Has 4 output classes:

     - 0 - neutral, no bad or good in input.
     - 1 - positive, at least one good, no bad in input.
     - 2 - negative, at least one bad, no good in input.
     - 3 - confused, at least one good and one bad in input.
    
    Can be tokenized by GreedyTokenizer. 
    """

    random.seed(a=seed)

    ret = []
    cls = []
    for i in range(num_rows):
        sent = []
        while len(sent) < row_length * 2:
            r = random.random()

            word = "neutral"

            if r > 0.9:
                word = "good"
            elif r > 0.8:
                word = "bad"
            elif r > 0.2:
                word = " "

            if word != " ":
                word = random.choice(SYNONYMS[word])

            sent.append(word)

        ret.append("".join(sent))

        gt = 0  # neutral
        if "good" in sent and "bad" in sent:
            gt = 3  # confused
        elif "good" in sent:
            gt = 1  # positive
        elif "bad" in sent:
            gt = 2  # negative

        cls.append(gt)

    return pd.DataFrame(dict(sentence=ret, sentiment=cls))


def generate_dataset_soft(num_rows: int, row_length: int, seed=0xdeadbeef):
    """
    Generate random sentiment sentences and their labels. Uses only the tokens
    "good", "bad", "neutral", and their synonyms but also creates words that
    combine these tokens. Output class is determined by which of the tokens
    appears most frequently. Can be tokenized by GreedyTokenizer. 
    """

    random.seed(a=seed)

    ret = []
    cls = []
    for i in range(num_rows):
        sent = []

        goods = 0
        bads = 0

        while len(sent) < row_length * 2:
            r = random.random()

            word = "neutral"

            if r > 0.9:
                word = "good"
                goods += 1
            elif r > 0.8:
                word = "bad"
                bads += 1
            elif r > 0.2:
                word = " "

            if word != " ":
                word = random.choice(SYNONYMS[word])

            sent.append(word)

        ret.append("".join(sent))

        if goods > bads:
            gt = 0
        elif bads > goods:
            gt = 1
        else:
            gt = random.randint(0, 1)

        cls.append(gt)

    return pd.DataFrame(dict(sentence=ret, sentiment=cls))


class GreedyTokenizer:
    # The following special tokens mimic use of huggingface tokenizers like Bert.

    # The following tokens must be unique.

    # Whitespace/separator.
    space_token = "[SPC]"

    # Input separator, used at end of an token input sequence
    sep_token = "[SEP]"

    # Unknown tokens, everything that is not a vocabulary word mapped to unknown.
    unk_token = "[UNK]"

    # Padding to input token sequences up to a fixed length.
    pad_token = "[PAD]"

    # Begining of input token. Token sequences start with this.
    cls_token = "[CLS]"

    # Regex for various separator characters including whitespace and punctuation.
    r_whitespace = r"(?P<whitespace>[\s\.\!\;\:])"

    # Regex for non-separator characters.
    r_blackspace = r"(?P<blackspace>\S)"

    def __init__(self, vocab, n_tokens: int = 8):
        self.vocab = vocab

        self.normal_tokens = [tok for tok in vocab.keys() if tok[0] != "["]

        # Regex for all normal (non-special) tokens.
        self.r_toks = "(?P<token>" + (
            "|".join(re.escape(tok) for tok in self.normal_tokens)
        ) + ")"

        self.n_tokens = n_tokens

        # Regex pattern for finding a token, a whitespace, or a non-whitespace.
        # It is important that non-whitespace comes after tokens as they are
        # potentially made of the same characters, with token having precedence.
        self.pattern = re.compile(
            (
                "|".join(
                    [
                        self.r_toks, GreedyTokenizer.r_whitespace,
                        GreedyTokenizer.r_blackspace
                    ]
                )
            )
        )

    def greedy_tokenize(self, text: str) -> List[nlp.Types.Span]:
        """
        Tokenize a text string into token spans in a greedy manner.
        """
        spans = []

        # Accumulators for constructing separator and unknown tokens. Regexp
        # reads whitespace and "blackspace" characters, one at a time, if no
        # token is found. These need to be accumulated into one large spacing or
        # unknown token.
        current_type = None

        # For every match of main pattern.
        for m in self.pattern.finditer(text.lower()):
            # Type of match (token/whitespace/blackspace)
            type = m.lastgroup
            # Matching string.
            tok = m.groupdict()[type]
            # Its span in input text.
            span = m.span(type)

            # Replace whitespace and blackspace matches with temporary special
            # token indicators.
            if type == "token":
                pass
            elif type == "whitespace":
                tok = self.space_token
            elif type == "blackspace":
                tok = self.unk_token

            # Accumulte separators and unknown tokens.
            if type != "token":
                if current_type == type:
                    spans[-1].end = span[1]
                else:
                    current_type = type
                    spans.append(
                        nlp.Types.Span(tok, begin=span[0], end=span[1])
                    )

            # Otherwise append a non-special token.
            else:
                spans.append(nlp.Types.Span(tok, begin=span[0], end=span[1]))
                current_type = None

        return spans

    def tokenize_into_tru_tokens(
        self, texts: List[str]
    ) -> nlp.Types.TruTokenization:
        toks = [self._tokenize_into_tru_tokens(text) for text in texts]
        return nlp.Types.TruTokenization.collate(toks)

    def _tokenize_into_tru_tokens(self, text: str) -> nlp.Types.TruTokenization:
        all_spans = self.greedy_tokenize(text)

        spans = []
        input_ids = []

        def add_special(tok):
            spans.append(nlp.Types.Span(item=tok, begin=0, end=0))
            input_ids.append(self.vocab[tok])

        add_special(self.sep_token)

        for span in all_spans:
            if span.item in [self.space_token]:
                pass
            else:
                spans.append(span)
                input_ids.append(self.vocab[span.item])

            if len(spans) + 1 >= self.n_tokens:
                break

        add_special(self.cls_token)

        while len(spans) < self.n_tokens:
            add_special(self.pad_token)

        return nlp.Types.TruTokenization(
            spans=[spans],
            token_ids=[input_ids],
        )

    def tokenize_into_tru_words(
        self, texts: List[str]
    ) -> nlp.Types.TruTokenization:
        toks = [self._tokenize_into_tru_words(text) for text in texts]
        return nlp.Types.TruTokenization.collate(toks)

    def _tokenize_into_tru_words(self, text: str) -> nlp.Types.TruTokenization:
        all_spans = self.greedy_tokenize(text)

        spans = []

        current_span = None

        for span in all_spans:
            if span.item in [self.space_token]:
                if current_span is not None:
                    spans.append(current_span)
                    current_span = None
                pass
            else:
                if current_span is None:
                    current_span = nlp.Types.Span(
                        item=str(span.item), begin=span.begin, end=span.end
                    )
                else:
                    current_span.item += span.item
                    current_span.end = span.end

            if len(spans) + 1 >= self.n_tokens:
                break

        if current_span is not None:
            spans.append(current_span)

        return nlp.Types.TruTokenization(spans=[spans])
