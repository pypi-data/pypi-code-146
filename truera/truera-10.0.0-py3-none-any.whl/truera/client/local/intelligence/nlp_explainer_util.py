# SMALL DEBT
'''
This file is used to circumvent typing issues in the nlp_explainer. Methods that
need typing and generally other nlp imports are defined here. We need this
because there are different packaging modes and the nlp imports are not always
available. This utils class can be imported from the explainer class within a
function to avoid import errors for the non-nlp package modes.
'''
import os
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
from trulens.nn.models import discern_backend
import yaml

from truera.client.local.intelligence.local_nlp_explainer import \
    LocalNLPExplainer
from truera.client.nn.client_configs import LayerAnchor
from truera.client.nn.client_configs import NLPAttributionConfiguration
from truera.client.nn.wrappers.datasets import convert_to_truera_iterable
from truera.client.nn.wrappers.hugs import TruNLPCounterfactualSplitLoadWrapper
from truera.nlp.general.model_runner_proxy.mem_utils import save_nlp_model_info
from truera.nlp.general.utils.configs import TokenType
from truera.rnn.general.container.artifacts import ArtifactsContainer
from truera.rnn.general.model_runner_proxy.sampling_utils import \
    prepare_datasplit


def _get_feature_influences_from_cache(
    nlp_explainer: LocalNLPExplainer,
    artifacts_container: ArtifactsContainer,
    num_records: int,
    token_type: TokenType = TokenType.WORD
) -> pd.DataFrame:
    """
        Wrapper function for nlp_explainer._compute_performance(). Computes
        various metrics on the label and predictions. To see the list of
        available metrics, use list_performance_metrics

        Args:
            - artifacts_container (ArtifactsContainer): The metadata of local
              artifacts.
            - num_records (int): The number of records to return
            - token_type (TokenType): the token aggregation type. Can be
              TokenType.Word or TokenType.TOKEN
            - qoi_type (QoIType): The type of QoI for multiclass. Defaults to
              QoIType.CLASS_WISE, but can be QoIType.MAX_CLASS.

        Returns:
            - pd.DataFrame: a dataframe of the original sentence, and influences
              per specified TokenType
        """

    output_path: Path = Path(
        nlp_explainer.sync_client.get_cache_path(artifacts_container.locator)
    )
    nlp_explainer._logger.debug(
        f'Output path for influences: {output_path.resolve()}'
    )
    influences = None
    try:
        influences = nlp_explainer._aiq.model.get_artifacts_df(
            artifacts_container, token_type=token_type, num_records=num_records
        ).drop(columns=["influences_comparative"])

    except FileNotFoundError:
        # if this failed, then the artifacts need to be generated
        nlp_explainer._logger.debug("Calculating feature influences")
        output_path.mkdir(parents=True, exist_ok=True)
    return influences, output_path


def _generate_feature_influences(
    nlp_explainer: LocalNLPExplainer,
    start: Optional[int] = 0,
    stop: Optional[int] = None,
    batch_size: int = 4,
    token_type: TokenType = TokenType.WORD,
    is_counterfactuals: bool = False
) -> pd.DataFrame:
    """
    A helper function that generates the input influences.

    Args:
        - nlp_explainer
        - start (int): A starting offset of the data records
        - stop (int): A stop offset of the data records
        - batch_size (int): The number of records in a influence calculation.
          This parameter is used to modify for speed vs memory constraints.
        - token_type (str): the token aggregation type. Can be "word" or "token"
        - is_counterfactuals (bool): A flag on if the influences are
          counterfactuals, which need different metadata and split loaders.
    Returns:
        - pd.DataFrame: a dataframe of the original sentence, and influences per
          specified TokenType
    """
    start, stop = nlp_explainer._convert_start_stop(
        start, stop, metrics_count=False
    )

    # Static methods only but we create instance anyway to simplify typing hints.
    model_load_wrapper = nlp_explainer._model.model_obj
    model_run_wrapper = nlp_explainer._model.model_run_wrapper

    model = model_load_wrapper.get_model()
    tokenizer = model_load_wrapper.get_tokenizer(model_run_wrapper.n_tokens)
    vocab: Dict[str, int] = tokenizer.vocab

    nlp_explainer._logger.debug('Loaded model and tokenizer.')
    backend = discern_backend(model)

    if not tokenizer.has_tokenspans and token_type == TokenType.WORD:
        raise ValueError(
            'Cannot use token_type="word" when tokenizer.tokenize_into_tru_tokens does not provide spans. Try token_type="token" instead.'
        )

    # pylint: disable=not-callable
    if is_counterfactuals:
        artifacts_container = nlp_explainer._artifacts_container_cf
    else:
        artifacts_container = nlp_explainer._artifacts_container

    artifact_locator = artifacts_container.locator
    output_path: Path = Path(
        nlp_explainer.sync_client.get_cache_path(artifact_locator)
    )

    # Counterfactuals dataset will not know about the original dataset
    # The only shared contract is that text will be an input.
    if is_counterfactuals:
        # Use Truera Wrappers because we have created a new dataset in a format only known to Truera
        split_load_wrapper = TruNLPCounterfactualSplitLoadWrapper(output_path)

    else:
        split_load_wrapper = nlp_explainer._data_collection.data_splits[
            nlp_explainer._base_data_split.name
        ].truera_wrappers.split_load_wrapper

    from truera.nlp.general.model_runner_proxy.nlp_attributions import \
        NLPAttribution

    # Define nlp attributor
    nlp_attributor = NLPAttribution()

    num_steps = 3

    # pylint: disable=no-member
    nlp_explainer._logger.debug(
        "Starting Split: " + nlp_explainer._base_data_split.name
    )

    #TODO: to get post model filters working
    filter_func = None

    sample_size: int = stop
    # Many times NN dataset object sizes are unknown, so a specific n_metrics_records is asked for.
    metrics_size: int = max(
        sample_size, nlp_explainer._attr_config.n_metrics_records
    )

    # This is being copied in case a re-downloaded project may want to recompute.
    run_config = dict()

    for k, v in nlp_explainer._attr_config.__dict__.items():

        if isinstance(v, LayerAnchor):
            v = LayerAnchor.to_string(v)
        run_config[k] = str(v)

    if 'logger' in run_config:
        run_config.pop('logger')

    with open(os.path.join(output_path, 'run_config.yaml'), 'w') as f:
        yaml.dump(run_config, f)
    nlp_explainer._logger.debug('Run config copied to output path.')

    nlp_explainer._logger.info("preparing datasplit")

    split_ds, batch_size, _ = prepare_datasplit(
        convert_to_truera_iterable(
            split_load_wrapper.get_ds(), batch_size=batch_size
        ),
        backend=backend,
        batch_size=batch_size,
        model=model,
        model_wrapper=model_run_wrapper,
        tokenizer_wrapper=tokenizer,
        standardize_fn=split_load_wrapper.standardize_databatch,
        num_take_records=metrics_size,
        shuffle=nlp_explainer._attr_config.shuffle_data
    )
    split_ds = split_ds.collect(
    )  # can now be iterated multiple times, but is fully stored in memory

    # n_influences can not be larger than actual split size
    sample_size: int = min(sample_size, len(split_ds))

    nlp_explainer._logger.info(f"=== Step 2/{num_steps}: Save Model Info ===")
    save_nlp_model_info(
        ds=split_ds,
        model_run_wrapper=model_run_wrapper,
        model=model,
        tokenizer=tokenizer,
        vocab=vocab,
        metrics_size=metrics_size,
        sample_size=sample_size,
        output_path=output_path,
        model_config=nlp_explainer._attr_config,
        backend=backend,
        forward_padded=False,
        filter_func=filter_func,
        split_load_wrapper=split_load_wrapper,
        logger=nlp_explainer._logger
    )

    # Disable counterfactual influence generation until this is needed: MLNN-9/MLNN-123
    nlp_explainer._logger.info(
        f"=== Step 3/{num_steps}: Input Attributions ==="
    )
    total_records = NLPAttribution.count_records(
        ds=split_ds, model=model, sample_size=sample_size, backend=backend
    )
    gradient_path_records = min(sample_size, total_records)

    nlp_attributor.calculate_attribution(
        split_ds=split_ds,  # "ds"
        batch_size=batch_size,
        model=model,
        tokenizer=tokenizer,
        model_run_wrapper=model_run_wrapper,
        output_path=output_path,
        sample_size=sample_size,
        model_args=nlp_explainer._attr_config,
        backend=backend,
        resolution=nlp_explainer._attr_config.resolution,
        gradient_path_sample_size=gradient_path_records,
        filter_func=filter_func
    )

    nlp_attributor.calculate_attribution_per_original_word(output_path)
    return nlp_explainer._aiq.model.get_artifacts_df(
        artifacts_container, token_type=token_type, num_records=stop
    ).drop(columns=["influences_comparative"])[start:stop]


def get_default_nlp_config() -> NLPAttributionConfiguration:
    attr_config = NLPAttributionConfiguration(
        baseline_type='',
        embedding_layer='',
        output_layer='',
        n_output_neurons=0,
        n_metrics_records=0,
        shuffle_data=False
    )
    return attr_config
