# VERY HIGH DEBT

from dataclasses import asdict
import json
import os
from pathlib import Path
import pickle
from typing import (
    Any, Callable, Dict, Iterable, Iterator, List, Optional, Sequence
)

import numpy as np
from tqdm.auto import tqdm
from trulens.nn.backend import Backend
import trulens.nn.backend as B
from trulens.nn.models import discern_backend
import yaml

from truera.client.nn import NNBackend as NNB
from truera.client.nn import wrappers as base
from truera.client.nn.client_configs import AttributionConfiguration
from truera.client.nn.client_configs import Dimension
from truera.client.nn.wrappers import nlp
from truera.rnn.general.model_runner_proxy.dimension_utils import \
    transpose_to_standard_dimensions
from truera.rnn.general.model_runner_proxy.explain_helpers import \
    evaluate_model_helper
from truera.rnn.general.model_runner_proxy.explain_helpers import \
    PostModelFilterProcessor
from truera.rnn.general.utils import log
from truera.utils.file_utils import as_path

Shape = Iterable[int]


class MemmapStreamer():

    def __init__(self, output_path: Path, sample_size: int):
        self.output_path: Path = as_path(output_path, warn=True)
        self.sample_size: int = sample_size
        self.memmap_fp: np.memmap = None
        self.total_records: int = 0

    def init_memmap_fp(
        self,
        name: str,
        single_arr_shape: Iterator[int],
        dtype: str = 'float32'
    ) -> None:

        self.memmap_fp = get_memmap_fp(
            self.output_path,
            name, [self.sample_size] + list(single_arr_shape),
            dtype=dtype
        )

    def memmap_is_init(self) -> bool:
        return not (self.memmap_fp is None)

    def memmap_is_full(self) -> bool:
        return self.total_records >= self.sample_size

    def append(self, arr: np.ndarray) -> None:
        new_records = min(len(arr), self.sample_size - self.total_records)
        if (new_records > 0):
            self.memmap_fp[self.total_records:self.total_records +
                           new_records] = arr[:new_records]
            self.total_records += new_records

    def close(self):
        del self.memmap_fp


def save_artifact_config(
    output_path: Path, forward_padded: bool, one_hot_sizes: bool, data_dtype
):
    p = as_path(output_path, warn=True)

    # Creates file:
    p_config = p / "artifact_config.yaml"

    # Creates file conditionally:
    p_transform = p / "feature_transform_map.json"

    feature_transformed = True if one_hot_sizes else False
    config = {
        'forward_padded': forward_padded,
        'feature_transformed': feature_transformed,
        'data_dtype': str(data_dtype),
    }

    log.debug(f"writing artifact config to {p_config}")
    with p_config.open('w') as h:
        yaml.dump(config, h)

    if feature_transformed:
        log.debug(f"writing feature transform to {p_transform}")
        with p_transform.open('w') as h:
            json.dump(one_hot_sizes, h)


def get_memmap_fp(
    output_path: Path,
    name: str,
    memmap_shape: Shape,
    dtype='float32'
) -> np.memmap:
    # TODO: document effects

    # Creates dir:
    p = as_path(output_path, warn=True)

    # Creates files:
    p_data = p / f"{name}.dat"
    p_shape = p / f"{name}_shape.npy"
    p_dtype_txt = p / f"{name}_dtype.txt"
    p_dtype_pkl = p / f"{name}_dtype.pkl"

    log.debug(f"making dirs {p}")
    p.mkdir(parents=True, exist_ok=True)

    fp = np.memmap(
        str(p_data), dtype=dtype, mode='w+', shape=tuple(memmap_shape)
    )

    # Save shape for memmap marshalling
    log.debug(f"writing numpy to {p_shape}")
    np.save(str(p_shape), np.asarray(memmap_shape))
    # Save dtype for memmap marshalling
    # Commonly dtype is in the form <class numpy.dtype.float32>. Pkl output is if downstream scripting needs to utilize the numpy class.
    log.debug(f"writing dtype pkl to {p_dtype_pkl}")
    with p_dtype_pkl.open('wb') as f:
        pickle.dump(dtype, f)

    # Also output the dtype string for human readability.
    log.debug(f"writing dtype txt to {p_dtype_txt}")
    with p_dtype_txt.open('w') as f:
        f.write(str(dtype))

    return fp


def save_pickle(output_path: Path, name: str, obj: Any) -> None:
    # Creates file:
    p = as_path(output_path, warn=True) / f"{name}.pkl"

    log.debug(f"writing pickle to {p}")

    with p.open("wb") as f:
        pickle.dump(obj, f)


def load_pickle(path: Path, name: str) -> Any:
    path = as_path(path, warn=True)

    with (path / f"{name}.pkl").open("rb") as f:
        dic = pickle.load(f)

    return dic


def save_memmap(
    output_path: Path,
    name: str,
    data_list: List[List[Any]],
    dtype='float32'
) -> None:
    # Creates file (conditionally):
    p_json = as_path(output_path, warn=True) / "feature_dtypes.json"

    num_records = 0
    for batch in data_list:
        for record in batch:
            num_records += 1

    # save original dtypes of each feature if varied
    if isinstance(dtype, str) and dtype == 'mixed':
        dtype = '<U16'  # encode as 16-char unicode
        single_slice_record = data_list[0][0][0]

        feature_dtypes = [type(f) for f in single_slice_record]

        log.debug(f"writing json to {p_json}")

        with p_json.open('w') as h:
            json.dump(feature_dtypes, h)

    assert len(data_list) > 0, "no instances were provided to save"
    assert len(data_list[0]) > 0, "provided instances are empty"

    memmap_shape = [num_records] + list(data_list[0][0].shape)

    fp: np.memmap = get_memmap_fp(output_path, name, memmap_shape, dtype=dtype)
    i = 0

    # TODO: document the effects happening here with np.memmap .
    for batch in data_list:
        for record in batch:
            fp[i] = record
            i += 1

    log.debug(name + ": " + str(fp.shape))
    del fp


def load_memmap(path: Path, name: str) -> np.ndarray:
    path = as_path(path, warn=True)

    memmap_shape = np.load(path / f"{name}_shape.npy")

    fp = np.memmap(
        path / (name + ".dat"),
        dtype='float32',
        mode='r',
        shape=tuple(memmap_shape)
    )

    return fp


# TODO: Type hints.
def get_batched_save_data(
    ds_batch: Any,
    *,
    model: NNB.Model,
    model_wrapper: base.Wrappers.ModelRunWrapper,
    model_config: AttributionConfiguration,
    backend: Backend,
    filter_func: Callable = None,
    tokenizer_wrapper: Optional[nlp.Wrappers.TokenizerWrapper] = None,
) -> Dict[str, Sequence[Any]]:
    """
    Uses batched data and returns a dictionary of items to be saved to
    artifacts.

    Args:
     - ds_batch (Any): A batch of model running data.
     - model (Model): The model object.
     - model_wrapper (Base.ModelRunWrapper): The ModelRunWrapper implementation.
     - model_config (AttributionConfiguration): The attribution configurations.
     - backend (Backend): The trulens backend.
     - filter_func (Callable, optional): A callable to filter records. Defaults
       to None.
     - tokenizer_wrapper (TokenizerWrapper, optional): The TokenizerWrapper
       implementation if this is an NLP domain. Defaults to None.

    Returns:
     Dict[str, Sequence[Any]]: A dictionary of keys and data to be saved.
    """
    is_nlp = tokenizer_wrapper is not None

    # TruBatch a dataclass in RNN, NLP
    def get(o, a):
        return getattr(o, a)

    def set(o, a, v):
        setattr(o, a, v)

    if backend is None:
        backend = discern_backend(model)

    os.environ['TRULENS_BACKEND'] = backend.name.lower()
    if is_nlp:
        assert isinstance(
            model_wrapper, nlp.Wrappers.ModelRunWrapper
        ), "ModelRunWrapper used does not inherit from nlp.Wrappers.ModelRunWrapper"
        tru_data: nlp.Types.TruBatch = model_wrapper.trubatch_of_databatch(
            ds_batch, model=model, tokenizer=tokenizer_wrapper
        )
        text_data: nlp.Types.TextBatch = model_wrapper.textbatch_of_trubatch(
            tru_data
        )
        token_data: nlp.Types.TruTokenization = tokenizer_wrapper.tokenize_into_tru_tokens(
            text_data
        )

        sequence_mask = token_data.token_ids != tokenizer_wrapper.pad_token_id

        truera_data = dict(
            index=tru_data.ids,
            labels=tru_data.labels,
            token_ids=token_data.token_ids,
            sequence_mask=sequence_mask,
            original_text=text_data,
            processed_text=text_data
        )

    else:
        truera_data: base.Types.TruBatch = model_wrapper.trubatch_of_databatch(
            ds_batch, model=model
        )
        truera_data = asdict(truera_data)

    if filter_func is not None:
        _, _, batch_preds, filtered_indices = filter_func(
            ds_batch, model, backend
        )
        batch_size = len(truera_data['index'])
        save_data = {
            k: PostModelFilterProcessor.filter_batched_data(
                truera_data[k], batch_size, filtered_indices, backend
            ) for k in truera_data
        }
    else:
        if is_nlp:
            # first create input batches

            inputbatch: nlp.Wrappers.Types.InputBatch = model_wrapper.inputbatch_of_textbatch(
                texts=list(text_data), model=model, tokenizer=tokenizer_wrapper
            )

            # Evaluating model in smaller batches than data has come in.
            batch_preds = inputbatch.map_batch(
                lambda batch: model_wrapper.evaluate_model(model, batch).
                probits,
                batch_size=model_config.rebatch_size
            )

        else:
            batch_preds = evaluate_model_helper(model_wrapper, ds_batch, model)

    save_data = {k: v for k, v in truera_data.items() if v is not None}
    save_data['batch_preds'] = batch_preds

    ##convert to np if neccessary
    # TODO: don't allow this ambiguity in produced data
    for k in save_data:
        if not isinstance(save_data[k], np.ndarray) and len(
            save_data[k]
        ) > 0 and not isinstance(save_data[k][0], str):

            save_data[k] = B.get_backend().as_array(save_data[k])

    if not is_nlp:
        standardize_save_data_dimension_order(save_data, model_config)

    return save_data


def standardize_save_data_dimension_order(save_data, model_config):
    input_dimension_order = model_config.input_dimension_order
    if 'features' in save_data:
        save_data['features'] = transpose_to_standard_dimensions(
            save_data['features'],
            (Dimension.BATCH, Dimension.TIMESTEP, Dimension.FEATURE),
            data_dimension_order=input_dimension_order
        )

    output_dimension_order = model_config.output_dimension_order
    if 'batch_preds' in save_data:
        save_data['batch_preds'] = transpose_to_standard_dimensions(
            save_data['batch_preds'],
            (Dimension.BATCH, Dimension.TIMESTEP, Dimension.CLASS),
            data_dimension_order=output_dimension_order
        )


# TODO: type hints
# TODO: come up with some arg grouping
def save_rnn_model_info(
    ds,
    model,
    model_wrapper,
    data_wrapper,
    metrics_size,
    sample_size: int,
    output_path: Path,
    model_config,
    backend,
    forward_padded: bool,
    filter_func=None
) -> None:
    output_path = as_path(output_path, warn=True)

    # Lists for saving results
    all_preds = []
    all_targets = []
    all_lengths = []
    all_keys = []
    all_data = []
    total_attributions = 0

    for ds_batch in tqdm(ds):
        if (total_attributions >= max(sample_size, metrics_size)):
            break

        save_data = get_batched_save_data(
            ds_batch,
            model=model,
            model_wrapper=model_wrapper,
            model_config=model_config,
            backend=backend,
            filter_func=filter_func
        )

        if (len(save_data['features']) <= 0):
            continue

        # Save artifacts, using preprocessed data if any transforms
        all_preds.append(save_data['batch_preds'])
        all_targets.append(save_data['labels'])
        all_lengths.append(save_data['lengths'])
        all_keys.append(save_data['ids'])
        data_key = 'preprocessed_features' if 'preprocessed_features' in save_data else 'features'
        if (total_attributions < sample_size):
            all_data.append(save_data[data_key])
        total_attributions += len(save_data[data_key])

    if model_config.n_time_step_output != model_config.n_time_step_input and model_config.n_time_step_output == 1:
        all_preds = [
            np.repeat(np.array(all_pred), model_config.n_time_step_input, 1)
            for all_pred in all_preds
        ]
        all_targets = [
            np.repeat(np.array(all_target), model_config.n_time_step_input, 1)
            for all_target in all_targets
        ]
    if len(all_keys[0].shape) == 1:
        all_keys = [all_key[:, None] for all_key in all_keys]

    one_hot_sizes = {}
    data_dtype = 'float32'

    if 'preprocessed_features' in save_data:
        one_hot_sizes = model_wrapper.get_one_hot_sizes()
        feature_dtype = save_data['preprocessed_features'].dtype
        data_dtype = 'mixed' if (feature_dtype == 'O') else feature_dtype

    save_artifact_config(output_path, forward_padded, one_hot_sizes, data_dtype)

    save_memmap(output_path, 'preds', all_preds)
    save_memmap(output_path, 'targets', all_targets)
    save_memmap(output_path, 'lengths', all_lengths)
    save_memmap(output_path, 'keys', all_keys, dtype='U32')
    save_memmap(output_path, 'data', all_data, dtype=data_dtype)

    if model_config.n_time_step_output != model_config.n_time_step_input and model_config.n_time_step_output == 1:
        save_memmap(output_path, 'output_lengths', np.ones_like(all_lengths))
    else:
        save_memmap(output_path, 'output_lengths', all_lengths)
