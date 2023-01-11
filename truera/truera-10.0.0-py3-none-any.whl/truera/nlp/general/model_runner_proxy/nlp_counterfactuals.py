# MEDIUM DEBT

import copy
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy import stats
import torch
from tqdm.auto import tqdm

from truera.nlp.general.model_runner_proxy.tokenizer_utils import \
    convert_back_newline_token
from truera.nlp.general.model_runner_proxy.tokenizer_utils import NEWLINE_TOKEN
from truera.rnn.general.container.artifacts import ArtifactsContainer
from truera.rnn.general.utils import log

log.configure(logging.INFO)
logger = log.logger


def filter_synonym_dict(synonym_dict: Dict[str, list], mlm_tokenizer):
    """
    filter synonym dict to only contain synonyms that can be tokenized into one token by the mlm tokenizer into a single token (cannot evaluate the 1-gram coherence score otherwise)
    and then attach the word ids for each synonym word
    synonym dict example: {token1:[synonym1_of_token1, synonym2_of_token1], token2:[synonym1_of_token2] ...}
    """
    filtered_synonym_dict = {}
    for w in synonym_dict:
        wn_filtered = []
        for wn in synonym_dict[w]:
            wn_tok = mlm_tokenizer.encode(wn, add_special_tokens=False)
            if len(wn_tok) == 1:
                wn_filtered.append((wn, wn_tok[0]))
        if len(wn_filtered) > 0:
            filtered_synonym_dict[w] = wn_filtered
    return filtered_synonym_dict


def get_augmented_counterfactual_table(
    labels: list,
    word_lists: List[List[str]],  # or np.ndarray?
    indices: List[int],
    synonym_dict: Dict[str, list],
    processed_text_column_name='Text',
    masked_text_column_name='MaskedText',
    label_column_name='Label',
    mask_token='[MASK]',
    n_sample=None
):
    """get a augmented table using synonym_dict (must be filtered first).
    infl original word[optional]: if provided, add the original combined influence of each original word to the dataframe.
    n_sample[optional]: if provided, sample a fixed amount of counterfactuals per original instance 
    and drop duplicates for instances with counterfactuals fewer than n_sample
    """
    data_counterfactual = {
        processed_text_column_name: [],
        masked_text_column_name: [],
        label_column_name: [],
        'original_index': [],
        'word_from': [],
        'word_to': [],
        'word_pos': [],
        'swapped_word_id': [],
    }
    for si, (s_split, ind, label) in tqdm(
        enumerate(zip(word_lists, indices, labels)),
        desc="computing augmented counterfactual table",
        unit="instance",
        total=len(word_lists)
    ):
        s_split = convert_back_newline_token(s_split)
        for wi, w in enumerate(s_split):
            wl = w.lower()
            if wl in synonym_dict and len(synonym_dict[wl]) != 0:
                for wr, wr_id in synonym_dict[wl]:
                    if w[0].isupper():
                        wr = wr.capitalize()
                    new_sentence = ' '.join(
                        [
                            ww if ii != wi else wr
                            for ii, ww in enumerate(s_split)
                        ]
                    )
                    masked_sentence_list = [
                        ww if ii != wi else mask_token
                        for ii, ww in enumerate(s_split)
                    ]
                    masked_sentence = ' '.join(masked_sentence_list)
                    word_pos = masked_sentence.index(mask_token)
                    data_counterfactual[processed_text_column_name].append(
                        new_sentence
                    )  ## use original tweet to be compatible with ingestionwrapper, can be made more general
                    data_counterfactual[masked_text_column_name].append(
                        masked_sentence
                    )
                    data_counterfactual[label_column_name].append(label)
                    data_counterfactual['original_index'].append(int(ind))
                    data_counterfactual['word_from'].append(w)
                    data_counterfactual['word_to'].append(wr)
                    data_counterfactual['word_pos'].append(word_pos)
                    data_counterfactual['swapped_word_id'].append(wr_id)
    df_counter = pd.DataFrame(data_counterfactual)
    if n_sample is not None:
        ### sampling counterfactuals
        df_cf = df_counter.groupby('original_index').sample(
            n=n_sample, replace=True, random_state=0
        )
        df_cf.drop_duplicates(inplace=True)
    else:
        df_cf = df_counter
    return df_cf


def get_coherence_score(
    mlm_model,
    mlm_tokenizer,
    df_cf: pd.DataFrame,
    device,  # TODO tensorflow
    masked_text_column_name='MaskedText',
    batch_size=16
):
    """
    get coherence score of each swapped_word_id by calculating the MLM prediction score of each swapped word id
    """

    # TODO tensorflow: this methods includes pytorch specific Tensor.to method .

    df_cf = df_cf.reset_index()
    df_cf_masked = df_cf.groupby([masked_text_column_name,
                                  'original_index']).agg(
                                      {
                                          'swapped_word_id': lambda x: list(x),
                                          'index': lambda x: list(x)
                                      }
                                  ).reset_index()
    num_batches = len(df_cf_masked) // batch_size + 1
    sentences = list(df_cf_masked.MaskedText)
    swapped_mlm_indices = list(df_cf_masked.swapped_word_id)
    original_indices = list(df_cf_masked.original_index)
    df_cf_indices = list(df_cf_masked['index'])
    all_probs = []
    for b in tqdm(
        range(num_batches), desc="run word swapping", unit="DataBatch"
    ):
        sentence_batch = sentences[b * batch_size:(b + 1) * batch_size]
        swapped_mlm_indices_batch = swapped_mlm_indices[b * batch_size:(b + 1) *
                                                        batch_size]
        original_indices_batch = original_indices[b * batch_size:(b + 1) *
                                                  batch_size]
        df_cf_indices_batch = df_cf_indices[b * batch_size:(b + 1) * batch_size]
        if len(sentence_batch) == 0:
            continue
        sentence_inputs = mlm_tokenizer(
            sentence_batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=300
        ).to(device)
        try:
            # Try with the supplied device. This should only have issues when cuda device is installed.
            # known problem is when torch has an unsupported CUDA arch, but the right version needs to be installed by the user.
            # Example Error:
            #     CUDA error: no kernel image is available for execution on the device
            #     NVIDIA A10G with CUDA capability sm_86 is not compatible with the current PyTorch installation.
            mask_indices = torch.where(
                sentence_inputs["input_ids"] == mlm_tokenizer.mask_token_id
            )
        except RuntimeError as e:
            cuda_install_cmd = "pip install torch==`<torch_version>`+cu`<cuda_version>` -f https://download.pytorch.org/whl/cu`<cuda_version>`/torch_stable.html"
            cuda_install_cmd_example = "pip install torch==1.12.1+cu116 -f https://download.pytorch.org/whl/cu116/torch_stable.html"

            current_torch = torch.__version__
            current_cuda = torch.version.cuda
            major_minor_current_capability = torch.cuda.get_device_capability(
                device
            )
            current_arch = f"sm_{major_minor_current_capability[0]}{major_minor_current_capability[1]}"
            supported_archs = torch.cuda.get_arch_list()
            logger.error(
                f"Encountered a runtime error. TruEra uses torch transformers to find counterfactuals so needs the right torch installed. \n"
                + f"Current architecture: {current_arch} \n" +
                f"Current torch version: {current_torch} \n" +
                f"Current cuda version: {current_cuda} \n" +
                f"Supported architectures (See: `torch.cuda.get_arch_list()`): {supported_archs}\n"
                +
                f"\nPlease install a torch cuda version that supports your GPU with: \n`{cuda_install_cmd}` \n"
                + f"\nExample: \n`{cuda_install_cmd_example}`"
            )
            raise e
        valid_index, mask_index = mask_indices[0].cpu().numpy(
        ), mask_indices[1].cpu().numpy()
        swapped_mlm_indices_batch = [
            swapped_mlm_indices_batch[vi] for vi in valid_index
        ]
        original_indices_batch = [
            original_indices_batch[vi] for vi in valid_index
        ]
        df_cf_indices_batch = [df_cf_indices_batch[vi] for vi in valid_index]
        sentence_inputs = {
            k: v[valid_index] for k, v in sentence_inputs.items()
        }
        if len(valid_index) > 0:
            with torch.no_grad():
                output = mlm_model(**sentence_inputs)
                probits = torch.nn.functional.softmax(
                    output.logits
                )[np.arange(len(valid_index)), mask_index, :]

            for predi, si, oi, di in zip(
                probits, swapped_mlm_indices_batch, original_indices_batch,
                df_cf_indices_batch
            ):
                all_probs.append((oi, si, di, predi[si]))
    coherence_score = np.zeros(len(df_cf))
    for oi, si, di, wi in tqdm(
        all_probs, desc="coherence scoring", unit="DataBatch"
    ):
        for dii, wii in zip(di, wi):
            coherence_score[dii] = wii
    return coherence_score


def calculate_counterfactual(
    aiq: "NlpAIQ", artifacts_container_original: ArtifactsContainer,
    output_path_counterfactual: Path, device: torch.device
):
    """Calculates counterfactuals from the original data by using torch transformer mlm model. 
    The counterfactuals are filtered (by coherence score) and a dataset.csv is saved to output_path_counterfactual

    Args:
        aiq (NlpAIQ): The aiq to help access artifacts.
        artifacts_container_original (ArtifactsContainer): The original artifacts metadata.
        output_path_counterfactual (Path): The location of the counterfactuals artifacts metadata.
        device (torch.device): The torch device.
    """

    from transformers import DistilBertForMaskedLM
    from transformers import DistilBertTokenizerFast

    distilbert_mlm_model_name = 'distilbert-base-uncased'
    mlm_tokenizer = DistilBertTokenizerFast.from_pretrained(
        distilbert_mlm_model_name
    )
    mlm_model = DistilBertForMaskedLM.from_pretrained(
        distilbert_mlm_model_name
    ).to(device)
    mlm_model.eval()
    mlm_model.zero_grad()

    with (Path(__file__).parent.absolute() / 'synonyms.json').open('rb') as f:
        synonym_dict = json.load(f)

    filtered_synonym_dict = filter_synonym_dict(synonym_dict, mlm_tokenizer)
    num_records = aiq.model.get_default_num_records(
        artifacts_container_original, influences=True
    )
    words: Tuple[List[List[str]], List[int]] = aiq.model.get_words(
        artifacts_container_original, num_records=num_records
    )
    ids = aiq.model.get_ids(
        artifacts_container_original, num_records=num_records
    )

    indices = np.concatenate(
        ids, 0
    )  #load_memmap(output_path_original, 'original_ids')
    labels = np.concatenate(
        aiq.model.get_ground_truth(
            artifacts_container_original, num_records=num_records
        ), 0
    )
    df_cf = get_augmented_counterfactual_table(
        labels,
        words[0],
        indices,
        filtered_synonym_dict,
        mask_token=mlm_tokenizer.mask_token
    )
    coherence_score = get_coherence_score(
        mlm_model, mlm_tokenizer, df_cf, device=device, batch_size=16
    )
    df_cf = df_cf.assign(coherence_score=pd.Series(coherence_score).values)

    # TODO: Figure out if there is a better way to choose this - ex: sort by best ones and pick the top.
    counterfactual_coherence_threshold = 0.02
    df_cf_filtered = df_cf[df_cf.coherence_score >
                           counterfactual_coherence_threshold
                          ]  ### coherence filtering

    logger.debug(
        f'df size before filtering: {len(df_cf)}, df size after filtering: {len(df_cf_filtered)}'
    )

    # This is the file for a "new" dataset. It can only be loaded with the TruNLPCounterfactualSplitLoadWrapper
    df_cf_filtered.to_csv(
        output_path_counterfactual / 'dataset.csv', encoding='L1'
    )


def find_diff_tokens(
    original_sequence: Sequence[Any], changed_sequence: Sequence[Any]
):
    """ Find the difference of two sequences that may have had modifications: add, remove, replace-many-to-one, replace-one-to-many

    Args:
        original_sequence (Sequence[Any]): The comparative sequence
        changed_sequence (Sequence[Any]): The modified sequence

    Returns:
        original_sequence_diff: The start and end indices of the diffed sequence.
        changed_sequence_diff: The start and end indices of the diffed sequence.
    """
    original_sequence = copy.deepcopy(list(original_sequence))
    changed_sequence = copy.deepcopy(list(changed_sequence))
    original_sequence.append('Token to Check End Sequence')
    changed_sequence.append('Token to Check End Sequence')
    diff_start = None
    for i in range(min(len(original_sequence), len(changed_sequence))):
        if original_sequence[i] != changed_sequence[i]:
            diff_start = i
            break
    if diff_start is None:
        return None, None

    original_sequence = original_sequence[diff_start:]

    for i in range(diff_start, len(changed_sequence)):
        diff_end = i - 1
        try:
            original_sequence_diff_end = original_sequence.index(
                changed_sequence[i]
            ) - 1
            break
        except ValueError:
            pass
            # diff is continued

    original_sequence_diff_end = original_sequence_diff_end + diff_start
    if original_sequence_diff_end < diff_start:
        original_sequence_diff_end = -1
    if diff_end < diff_start:
        diff_end = -1
    return (diff_start, original_sequence_diff_end), (diff_start, diff_end)


def merge_lists_with_swaps(
    *, infs: Sequence[float], tokens: Sequence[str], diff_start: int,
    diff_end: int
) -> Tuple[Sequence[float], Sequence[str]]:
    """Consolidates list items that are part of a counterfactual swap. 

    Args:
        infs (Sequence[float]): The influenes per token
        tokens (Sequence[str]): The tokens
        diff_start (int): The start token index of a counterfactual swap
        diff_end (int): The end token index of a counterfactual swap

    Returns:
        infs: Modified infs list with the counterfactual swap tokens merged via sum.
        tokens: Modified tokens list with the counterfactual swap tokens merged via str concat.
    """
    if diff_end == -1:
        new_inf_list = copy.deepcopy(list(infs))
        new_inf_list.insert(diff_start, 0)

        new_token_list = copy.deepcopy(list(tokens))
        new_token_list.insert(diff_start, '[REMOVED]')
    else:
        sum_inf = sum(infs[diff_start:diff_end + 1])
        new_inf_list = list(infs[:diff_start]) + [sum_inf
                                                 ] + list(infs[diff_end + 1:])
        joined_token = ' '.join(tokens[diff_start:diff_end + 1])
        if diff_end - diff_start > 0:
            joined_token = '[' + joined_token + ']'
        new_token_list = tokens[:diff_start] + [joined_token
                                               ] + tokens[diff_end + 1:]
    return new_inf_list, new_token_list


def match_counterfactual_artifacts(text_df: pd.DataFrame):
    """
    match the artifacts between counterfactual and original ( so that correlation between them can be evaluated).
    """
    corrs = []
    swap = []
    swap_cf = []
    for i in range(len(text_df)):
        tokens = text_df['tokens'].iloc[i]
        tokens_cf = text_df['tokens_cf'].iloc[i]
        influences = text_df['influences'].iloc[i][0]
        influences_cf = text_df['influences_cf'].iloc[i][0]
        lengths = text_df['lengths'].iloc[i]
        lengths_cf = text_df['lengths_cf'].iloc[i]
        influences = influences[:lengths]
        influences_cf = influences_cf[:lengths_cf]
        original_sequence_diff, cf_sequence_diff = find_diff_tokens(
            tokens, tokens_cf
        )
        if original_sequence_diff is None:
            swap.append(None)
            swap_cf.append(None)
        else:
            (diff_start, original_sequence_diff_end) = original_sequence_diff
            (diff_start, diff_end) = cf_sequence_diff
            swap.append((diff_start, original_sequence_diff_end))
            swap_cf.append((diff_start, diff_end))
            influences, tokens = merge_lists_with_swaps(
                infs=influences,
                tokens=tokens,
                diff_start=diff_start,
                diff_end=original_sequence_diff_end
            )
            influences_cf, tokens_cf = merge_lists_with_swaps(
                infs=influences_cf,
                tokens=tokens_cf,
                diff_start=diff_start,
                diff_end=diff_end
            )
        if len(influences) == len(influences_cf):
            influences = np.asarray(influences)
            influences_cf = np.asarray(influences_cf)
            zeros_filter = np.logical_not(
                np.logical_and(influences == 0, influences_cf == 0)
            )
            corrs.append(
                stats.spearmanr(
                    influences[zeros_filter], influences_cf[zeros_filter]
                ).correlation
            )

        else:
            corrs.append(-2)

    text_df["swap"] = swap
    text_df["swap_cf"] = swap_cf
    text_df["corrs"] = corrs

    return text_df
