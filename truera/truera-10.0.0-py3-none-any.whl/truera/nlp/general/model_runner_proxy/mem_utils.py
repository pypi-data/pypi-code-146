from collections import defaultdict
import logging
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional

import numpy as np
import pandas as pd
from trulens.nn.backend import Backend

from truera.client.nn import NNBackend as NNB
from truera.client.nn.client_configs import NLPAttributionConfiguration
from truera.client.nn.wrappers.nlp import Types
from truera.client.nn.wrappers.nlp import Wrappers
from truera.client.util.iter_utils import LenIterable
from truera.nlp.fairness.utils import get_segment_per_text
from truera.nlp.general.model_runner_proxy.tokenizer_utils import \
    get_tokens_to_words_mapping
from truera.rnn.general.model_runner_proxy.mem_utils import \
    get_batched_save_data
from truera.rnn.general.model_runner_proxy.mem_utils import save_memmap
from truera.rnn.general.model_runner_proxy.mem_utils import save_pickle
from truera.rnn.general.utils import log
from truera.utils.file_utils import as_path


def update_occurrence_dict_batch(
    token_list, num_classes, labels, ids, original_dict
):
    """
    undate the token occurence dict by going through each batch of data 
    and appending the data id of the instances containing each token
    (the token_list can be the list of sentences or list of input ids)
    """
    for label in range(num_classes):
        if num_classes > 1:
            label_inds = np.where(labels == label)[0]
        else:
            label_inds = np.arange(len(ids))
        id_label = ids[label_inds]
        tokens_list_label = [token_list[i] for i in label_inds]
        for si, (s, idi) in enumerate(
            zip([np.unique(arr) for arr in tokens_list_label], id_label)
        ):
            for t in s:
                original_dict[t][label].append(int(idi))


def save_text_data(
    output_path: Path, name: str, data_list: Iterable[str]
) -> None:
    """Save a collection of strings."""

    # Creates file:
    p = as_path(output_path, warn=True) / f"{name}.csv"

    # Using pandas for the automatic newline escaping.
    csv = pd.DataFrame(data_list, columns=['text'])

    log.debug(f"writing text data to {p}")

    csv.to_csv(p)


def load_text_data(path: Path, name: str) -> List[str]:
    """Load a collection of strings."""

    p = as_path(path) / f"{name}.csv"

    csv = pd.read_csv(p)
    return csv.text.to_list()


# TODO: cleanup monster method
# TODO: type hints
def save_nlp_model_info(
    *,
    ds: LenIterable[Types.DataBatch],
    model_run_wrapper: Wrappers.ModelRunWrapper,
    model: NNB.Model,
    tokenizer: Wrappers.TokenizerWrapper,
    vocab: Dict[Types.Token, Types.TokenId],
    metrics_size: int,
    sample_size: int,
    output_path: Path,
    model_config: NLPAttributionConfiguration,
    backend: Backend,
    forward_padded: bool,  # not used
    filter_func: Callable = None,
    logger: logging.Logger = None,
    **split_load_wrapper_arg,
) -> None:
    # TODO: remove logic not related to saving from this method
    """Saves metric related artifacts to the output_path.

    Args:
        - ds (LenIterable[NLP.Types.DataBatch]): The dataset from
          ModelLoadWrapper.get_ds.
        - model_run_wrapper (NLP.ModelRunWrapper): The ModelRunWrapper
          implementation.
        - model (Model): The model object.
        - tokenizer (NLP.TokenizerWrapper): The TokenizerWrapper implementation.
        - vocab (Dict[Token, TokenId]): The token to its id map.
        - metrics_size (int): The number of records in metrics calculations.
        - sample_size (int): The number of records in non-metrics calculations.
        - output_path (Path): The output artifacts path.
        - model_config (NLPAttributionConfiguration): The attribution
          configurations.
        - backend (Backend): A trulens backend.
        - forward_padded (bool): Whether the data is forward padded. Currently
          unused and assumes backwards padding.
    """
    # TODO: Consider having this function in nlp_utils? Moved this import here since it needs transformers which is very nlp specific.

    split_load_wrapper = split_load_wrapper_arg["split_load_wrapper"]

    # Lists for saving results
    all_ids = []
    all_preds = []
    all_targets = []
    all_token_ids = []
    all_words = []
    all_tokens = []
    all_index_mappings = []
    all_original_text = []
    all_sequence_mask = []
    all_segments = []
    all_sentence_length_tokens = []
    # Evaluate loop
    total_attributions = 0
    occurrence_dict_token = defaultdict(
        lambda: [[] for _ in range(model_config.n_output_neurons)]
    )
    occurrence_dict_word = defaultdict(
        lambda: [[] for _ in range(model_config.n_output_neurons)]
    )

    for batch in ds.items(
        tqdm_options=dict(desc="saving data", unit="DataBatch")
    ):
        # TODO: fix inefficiency here. Batched into model-appropriate batches at
        # this point even though there is a lot of out-of-model processing
        # happening here.
        if total_attributions >= max(sample_size, metrics_size):
            break

        # tru_batch = model_run_wrapper.trubatch_of_databatch(batch)

        save_data = get_batched_save_data(
            batch,
            model=model,
            model_wrapper=model_run_wrapper,
            model_config=model_config,
            backend=backend,
            filter_func=filter_func,
            tokenizer_wrapper=tokenizer,
        )
        if len(save_data["index"]) <= 0:
            continue

        # Save artifacts

        all_ids.append(save_data["index"])
        all_preds.append(save_data["batch_preds"])
        all_targets.append(save_data["labels"].astype(int))
        all_original_text.extend(save_data["original_text"])

        sentence_length_tokens = save_data["sequence_mask"].sum(-1).astype(int)
        all_sentence_length_tokens.append(sentence_length_tokens)

        trutok = tokenizer.tokenize_into_tru_tokens(save_data['original_text'])
        tokenspan_lists: List[List[Types.Span[Types.Token]]] = trutok.spans
        token_list: List[List[Types.Token]] = trutok.token_ids

        if tokenspan_lists is not None:
            # Optional: enabled by providing token spans
            index_mappings, word_list = get_tokens_to_words_mapping(
                tokenspan_lists,
                save_data['original_text'],
                tokenizer,
                logger=logger
            )
            all_index_mappings.extend(index_mappings)

        else:
            wordsep_lists: List[List[Types.Span[Types.Word]]
                               ] = tokenizer.tokenize_into_tru_words(
                                   save_data['original_text']
                               ).spans
            word_list = [
                [wordsep.item
                 for wordsep in wordsep_list]
                for wordsep_list in wordsep_lists
            ]

        all_words.extend(word_list)
        all_tokens.extend(token_list)

        update_occurrence_dict_batch(
            word_list, model_config.n_output_neurons,
            save_data["labels"].astype(int),
            np.array(save_data["index"], dtype=np.int32), occurrence_dict_word
        )

        update_occurrence_dict_batch(
            [tokenizer.tokens_of_ids(iid) for iid in save_data["token_ids"]],
            model_config.n_output_neurons, save_data["labels"],
            np.array(save_data["index"], dtype=np.int32), occurrence_dict_token
        )
        all_token_ids.append(save_data["token_ids"])
        all_sequence_mask.append(save_data["sequence_mask"])
        total_attributions += len(save_data["token_ids"])

    save_text_data(output_path, "original_text", all_original_text)
    save_pickle(output_path, "words", all_words)
    save_pickle(output_path, "tokens", all_tokens)
    save_pickle(output_path, "token_to_id", vocab)
    id_to_token = {vocab[token]: token for token in vocab}
    save_pickle(output_path, "id_to_token", id_to_token)
    save_pickle(output_path, "index_mappings", all_index_mappings)
    save_pickle(output_path, "token_occurrence", dict(occurrence_dict_token))
    save_pickle(output_path, "word_occurrence", dict(occurrence_dict_word))
    save_memmap(output_path, "preds", all_preds)
    save_memmap(output_path, "targets", all_targets)
    save_memmap(output_path, "token_ids", all_token_ids)
    save_memmap(
        output_path, "original_ids", all_ids, dtype=int
    )  # TODO: IDs need to be strings eventually
    save_memmap(output_path, "sequence_mask", all_sequence_mask)
    save_memmap(
        output_path, "sentence_length_tokens", all_sentence_length_tokens
    )

    if issubclass(
        split_load_wrapper.__class__,
        Wrappers.SplitLoadWrapper.WithSegmentByWord
    ):
        segment_keywords_map = split_load_wrapper.get_segment_keywords_map()

        all_segment_names = get_segment_per_text(
            all_original_text, segment_keywords_map
        )

        segment_keys = sorted(list(segment_keywords_map.keys()))
        segment_name_to_id_map = {}

        for idx, segment_name in enumerate(segment_keys):
            segment_name_to_id_map[segment_name] = idx

        all_segments = [
            np.array(
                [
                    segment_name_to_id_map[segment_name]
                    for segment_name in all_segment_names
                ]
            )
        ]

        save_memmap(output_path, "segments", all_segments)
        save_pickle(output_path, "segment_keywords", segment_keywords_map)
