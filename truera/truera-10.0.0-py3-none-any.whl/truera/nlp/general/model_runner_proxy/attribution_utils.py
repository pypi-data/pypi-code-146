import logging
from typing import List

import numpy as np
from tqdm.auto import tqdm

from truera.client.nn.wrappers.nlp import Types
from truera.rnn.general.utils import log

log.configure(logging.INFO)


def combine_tokenized_influence_per_original_word(
    text_list: List[Types.Text],  # for debugging messages only
    word_list: List[List[Types.Word]],  # 
    token_list: List[List[Types.Token]],  #
    token_attrs: np.ndarray,
    index_mappings: list,
    combine_function=lambda x: x.sum(0),  ## combine the word/token dimension
):
    """
    word_list: a list of original words. 

    Combine token influence or grad_path influence of tokens into those original
    words. token_attr can have a shape of (num_instance, num_class, num_token)
    for token influence or (num_instance, num_class, num_token, num_resolution)
    for grad_path influence


    - word_list: a batch or sentences in word list form.

    - index_mappings: mappings from the word_indices to token indices. 

    - combine_function: a function to combine token indices mapped to the same
      word. Default is `np.sum` .
    """

    match_subword_fail_count = 0

    num_class = token_attrs.shape[1]
    if len(
        token_attrs.shape
    ) == 4:  ## grad_path_influence has one more dimension
        num_resolution = token_attrs.shape[-1]
        is_grad_path_influence = True
    else:
        is_grad_path_influence = False

    sentence_length_words = np.array([len(s) for s in word_list])

    original_word_attr_array_shape = (
        len(token_attrs), 1, num_class, np.max(sentence_length_words)
    )
    if is_grad_path_influence:  ## grad_path_influence has one more dimension
        original_word_attr_array_shape += (num_resolution,)

    original_word_attr_array = np.zeros(original_word_attr_array_shape)
    if len(index_mappings) == 0:
        log.info(
            "Detected that word spans were not ingested. Skipping word influences."
        )
    else:
        for sentence_index, (text, words, tokens, token_attr,
                             index_mapping) in tqdm(
                                 enumerate(
                                     zip(
                                         text_list, word_list, token_list,
                                         token_attrs, index_mappings
                                     )
                                 ),
                                 desc="aggregating influence",
                                 unit="instance",
                                 total=len(token_attrs)
                             ):
            text: Types.Text
            words: List[Types.Word]
            tokens: List[Types.Token]
            token_attr: np.ndarray
            index_mapping: List[List[int]]

            if len(index_mapping) == 0:
                raise ValueError(
                    "Had empty index mapping. Could not match any words to tokens:"
                    f"\nwords={words}"
                    f"\ntokens={tokens}"
                )

            unmatched_word_indices = []

            for word_index in range(len(index_mapping)):
                token_indices: List[int] = index_mapping[word_index]

                if len(token_indices) > 0:

                    infl_combined = [
                        combine_function(token_attr[qi, token_indices])
                        for qi in range(num_class)
                    ]

                    if is_grad_path_influence:
                        original_word_attr_array[
                            sentence_index, 0, :,
                            word_index, :] = np.array(infl_combined)
                    else:
                        original_word_attr_array[
                            sentence_index, 0, :,
                            word_index] = np.array(infl_combined)

                else:
                    match_subword_fail_count += 1
                    unmatched_word_indices.append(word_index)

            if len(unmatched_word_indices) > 0:
                log.info(
                    '***** some words were not matched to any token: \
                    \n instance index: {} \
                    \n instance: \n===\n{}\n===\
                    \n unmatched_words: {} \
                    \n; will automatically assigning zero influence:****\n'.
                    format(
                        sentence_index, text, ", ".join(
                            [
                                f"{repr(words[i])}[{i}]"
                                for i in unmatched_word_indices
                            ]
                        )
                    )
                )

        if match_subword_fail_count > 0:
            log.info(
                '**** number of failed matches {} in {} instances****\n'.format(
                    match_subword_fail_count, len(word_list)
                )
            )

    return original_word_attr_array.astype(np.float32)
