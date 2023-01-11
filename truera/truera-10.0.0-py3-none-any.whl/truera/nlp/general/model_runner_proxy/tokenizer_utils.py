from collections import deque
import logging
from typing import Dict, Iterable, List, Sequence

import numpy as np

from truera.client.nn.wrappers.nlp import Types
from truera.client.nn.wrappers.nlp import Wrappers

# TODO: might be deprecated
NEWLINE_TOKEN = '[NL]'


# TODO: might be deprecated
def convert_back_newline_token(words: List[str]):
    """
    convert newline token back to \n for counterfactual analysis
    """
    return [
        w if NEWLINE_TOKEN not in w else w.replace(NEWLINE_TOKEN, '\n')
        for w in words
    ]


def get_tokens_to_words_mapping(
    tokenspan_lists: Sequence[Types.Span[Types.Token]],
    texts_list: Sequence[Types.Text],
    tokenizer: Wrappers.TokenizerWrapper,
    logger: logging.Logger = None,
    warn=False
) -> Dict[int, Sequence[int]]:
    """ Using the token spans, match the token ids to the word ids.

    Args:
        tokenspan_lists (Sequence[Types.Span[Types.Token]]): The list of token spans.
        texts_list (Sequence[Types.Text]): The original texts.
        tokenizer (Wrappers.TokenizerWrapper): The tokenizer wrapper for tokenization utility.
        logger (logging.Logger, optional): For logging. Defaults to None.
        warn (bool, optional): Whether to show warnings. Defaults to False.

    Returns:
        Dict[int, Sequence[int]]: A dictionary with word ids as keys and a list of token ids as values.
    """

    # chomped text has everything beyond tokenization removed
    chomped_text: List[
        Types.Text
    ] = chomp_beyond_tokenization(tokenspan_lists, texts_list, logger=logger)
    trutok_chopped = tokenizer.tokenize_into_tru_words(chomped_text)
    wordsep_lists: List[List[Types.Span[Types.Word]]] = trutok_chopped.spans

    word_list = [
        [wordsep.item
         for wordsep in wordsep_list]
        for wordsep_list in wordsep_lists
    ]
    index_mappings = [
        word_to_token_map(tokenizer, words, tokens, text, warn=warn) for words,
        tokens, text in zip(wordsep_lists, tokenspan_lists, chomped_text)
    ]
    return index_mappings, word_list


def word_to_token_map(
    special_tokens: Sequence[str],
    words: Iterable[Types.Span[Types.Word]],
    tokens: Iterable[Types.Span[Types.Token]],
    text: Types.Text,  # for warning messages only
    warn: bool = False
) -> List[List[int]]:
    """ For a single record, use the token spans and match the token ids to the word ids.

    Args:
        special_tokens (Sequence[str]): Used for special token warnings.
        words (Iterable[Types.Span[Types.Word]]): Spans of the words.
        tokens (Iterable[Types.Span[Types.Token]]): Spans of the tokens.
        text (Types.Text): The original text

    Returns:
        List[List[int]]: The list of token ids per word.
    """
    # TODO: warn is usually when tokens are skipped in the mapping. This is not shown to user because word
    # definitions are truera defined so they shouldn't need to adjust their tokens to our word definitions.
    # If this becomes an issue (ie words not getting attributed right), we should figure out when to surface
    # this to a user, and how to not scare users from our internal span representations. MLNN-406
    maps = []
    tokens = deque(enumerate(tokens))
    for word in words:
        # Find the set of tokens (by their indices in the token list) that make up each word.

        map_for_word = []

        while True:
            # Pop tokens from the token deque while their span is within the word's span or break otherwise.

            if len(tokens) == 0:
                # No more tokens in deque.
                break

            tok_index, tok = tokens[0]  # peek the next token
            if tok.begin == tok.end:
                # advance token
                tokens.popleft()
            elif tok.end <= word.begin:
                if tok.item not in special_tokens:
                    if warn:
                        print(
                            f"WARNING: non-special token \"{tok}\" is not part of any word."
                        )

                # advance token
                tokens.popleft()
                continue

            elif tok.begin >= word.end:
                # If the next token spans past the word, break out of the token loop to finish that word's map.

                # advance word
                break

            elif tok.begin < word.begin or tok.end > word.end:
                if warn:
                    print(
                        f"WARNING: token {tok} spans more than one word. Truera will not consider it a part of any word."
                    )

                # advance token
                tokens.popleft()
                continue

            else:
                # token and word intersect in span
                map_for_word.append(tok_index)
                tokens.popleft()

        if len(map_for_word) == 0:
            if warn:
                # This will happen a lot of tokenization is limited in number of tokens and texts are long.
                print(
                    f"WARNING: could not find any tokens making up word \"{word}\" in:\n{text}"
                )
                pass

        maps.append(map_for_word)

    return maps


def chomp_beyond_tokenization(
    token_spans: List[List[Types.Span[Types.Token]]],
    texts: List[Types.Text],
    logger: logging.Logger = None
) -> List[Types.Text]:
    """
    Given a tokenization with spans of the given texts, chop off everything in
    those texts beyond what was tokenized (when number of tokens is limited).
    """

    max_indices = [max([span.end for span in spans]) for spans in token_spans]
    for spans, text, max_index in zip(token_spans, texts, max_indices):
        if max_index <= 0 and logger:
            logger.warn(
                f"When trying to pair tokens to words, spans show the max length to be 0. \nText:{text}\Spans:{spans}"
            )
    return [
        str(text[0:max_index]) for text, max_index in zip(texts, max_indices)
    ]


def tru_tokenization_to_offsets(
    tokenization: Types.TruTokenization[Types.Token]
) -> np.ndarray:
    """Get an np.ndarray of the tokenization offets. This is typically how a user will give us this data.

    Args:
        tokenization (Types.TruTokenization[Types.Token]): The truera internal representation of tokenization

    Returns:
        np.ndarray: array of dimensions (batch x spans x offsets)
    """
    return np.asarray(
        [
            [[span.begin, span.end]
             for span in spans]
            for spans in tokenization.spans
        ]
    )


def tru_tokenization_to_ids(
    tokenization: Types.TruTokenization[Types.Token]
) -> np.ndarray:
    """Get an np.ndarray of the token uds. This is typically how a user will give us this data.

    Args:
        tokenization (Types.TruTokenization[Types.Token]): The truera internal representation of tokenization

    Returns:
        np.ndarray: array of dimensions (batch x token_ids)
    """
    return np.asarray(
        [
            [token_id
             for token_id in token_ids]
            for token_ids in tokenization.token_ids
        ]
    )
