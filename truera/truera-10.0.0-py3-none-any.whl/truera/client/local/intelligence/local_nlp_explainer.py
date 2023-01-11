from __future__ import annotations

import logging
import os
from typing import (
    Any, Dict, Mapping, Optional, Sequence, Tuple, TYPE_CHECKING, Union
)

from cachetools import cached
from cachetools import LRUCache
import numpy as np
import pandas as pd
from scipy.special import logit

from truera.client.errors import FeatureDisabledException
from truera.client.intelligence.explainer import NonTabularExplainer
from truera.client.local.local_artifacts import Cache
from truera.client.local.local_artifacts import DataCollection
from truera.client.local.local_artifacts import Model
from truera.client.local.local_artifacts import Project
from truera.client.nn import NNBackend as NNB
from truera.client.nn import wrappers as base
from truera.client.nn.client_configs import AttributionConfiguration
from truera.client.nn.client_configs import DEFAULT_NN_HASH_BG
from truera.client.nn.client_configs import NLPAttributionConfiguration
from truera.client.nn.wrappers import nlp
from truera.client.nn.wrappers.datasets import convert_to_truera_iterable
from truera.client.truera_workspace_utils import ExplainerQiiCacheKey
from truera.nlp.general.utils.configs import TokenType
from truera.protobuf.public.metadata_message_types_pb2 import \
    ModelType  # pylint: disable=no-name-in-module
from truera.protobuf.public.qoi_pb2 import \
    ExplanationAlgorithmType  # pylint: disable=no-name-in-module

if TYPE_CHECKING:
    from truera.client.nn.wrappers import nlp


class LocalNLPExplainer(NonTabularExplainer):
    #TODO: conform nlp explainer signatures to other explainer type signatures.
    def __init__(
        self, model: Model, data_collection: DataCollection, data_split: str,
        project: Project, attr_config: NLPAttributionConfiguration,
        explanation_cache: Cache, logger: logging.Logger
    ):
        from truera.nlp.general.aiq.aiq import NlpAIQ
        from truera.nlp.general.container.model import NLPModelProxy
        from truera.nlp.general.utils.configs import TokenType

        super().__init__(
            model=model,
            data_collection=data_collection,
            data_split=data_split,
            project=project,
            attr_config=attr_config,
            explanation_cache=explanation_cache,
            logger=logger
        )

        #TODO: Migrate to NLP nn.wrappers.
        self._model_proxy = NLPModelProxy()
        self._aiq = NlpAIQ(model=self._model_proxy)
        self._token_type = TokenType
        self._qiis = None
        self.set_base_data_split(data_split)

    def _get_score_type(self) -> str:
        return self._project.score_type

    def _get_output_classes(self) -> int:
        return self._attr_config.n_output_neurons

    def _virtual_model_breakage_check(self, breakage_message):
        model_load_wrapper = self._model.model_obj
        if model_load_wrapper == ModelType.VIRTUAL:
            self._logger.error(
                f"The model loaded is a virtual model and {breakage_message}. This can happen if a virtual model was uploaded then downloaded. To fix, either re-add the model or upload and re-download a non-virtual model."
            )
            return True
        return False

    def _check_valid_token_type(self, token_type: str) -> TokenType:
        """Check if words were generated and the user supplied token_type. if token_type is None, auto detect the token type.
        If the token type requested is word but are not available, raise an error.

        Args:
            artifacts_container (ArtifactsContainer): The artifacts metadata.
            token_type (str): The requested token type. Can be "word", "token", or None. If None, auto-detect the type.
        """
        artifacts_container = self._artifacts_container
        if self._aiq.model.has_words(
            artifacts_container
        ) and token_type is None:
            self._logger.info(
                "token_type not supplied. Assuming token_type 'word' since 'word' influences are generated."
            )
            return TokenType.WORD
        elif not self._aiq.model.has_words(
            artifacts_container
        ) and token_type is None:
            self._logger.info(
                "token_type not supplied. Assuming token_type 'token' since 'word' influences are not generated."
            )
            return TokenType.TOKEN
        elif not self._aiq.model.has_words(
            artifacts_container
        ) and token_type == "word":
            raise FeatureDisabledException(
                "This feature is unavailable for token_type='word'. Try token_type='token'. This can happen if spans were not supplied at ingestion and influence generation."
            )
        else:
            token_type_enum = TokenType.from_str(token_type)
            return token_type_enum

    def _get_batches(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        batch_size: int = 4,
        batch_type: str = "data"
    ) -> Sequence[nlp.Types.TruBatch]:
        from trulens.nn.models import discern_backend

        from truera.rnn.general.model_runner_proxy.sampling_utils import \
            prepare_datasplit

        # Static methods only but we create instance anyway to simplify typing hints.
        model_load_wrapper = self._model.model_obj
        from_text_model_run_wrapper = self._model.model_run_wrapper

        model = model_load_wrapper.get_model()
        tokenizer = model_load_wrapper.get_tokenizer(
            from_text_model_run_wrapper.n_tokens
        )

        self._logger.debug('Loaded model and tokenizer.')
        backend = discern_backend(model)
        os.environ['TRULENS_BACKEND'] = backend.name.lower()

        split_load_wrapper = self._data_collection.data_splits[
            self._base_data_split.name].truera_wrappers.split_load_wrapper
        model_run_wrapper = self._model.model_run_wrapper

        start, stop = self._convert_start_stop(start, stop)

        split_ds, batch_size, _ = prepare_datasplit(
            convert_to_truera_iterable(split_load_wrapper.get_ds()),
            backend=backend,
            batch_size=batch_size,
            model=model,
            model_wrapper=model_run_wrapper,
            tokenizer_wrapper=tokenizer,
            standardize_fn=split_load_wrapper.standardize_databatch,
            num_take_records=stop,
            shuffle=self._attr_config.shuffle_data
        )
        split_ds = split_ds.collect(
        )  # can now be iterated multiple times, but is fully stored in memory

        for data_batch in split_ds.items(tqdm_options=dict(unit="DataBatch")):
            if batch_type == "data":
                yield data_batch
            elif batch_type == "tru":
                yield model_run_wrapper.trubatch_of_databatch(
                    data_batch, model=model, tokenizer=tokenizer
                )

    @cached(cache=LRUCache(maxsize=16))
    def get_xs(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        extra_data: bool = False,
        system_data: bool = False,
        batch_size: int = 4
    ) -> pd.DataFrame:
        tru_batches = self._get_batches(
            start=start, stop=stop, batch_size=batch_size, batch_type="tru"
        )
        ids = []
        texts = []
        for curr in tru_batches:
            ids.append(curr.ids)
            texts.append(curr.text)
        ids = np.concatenate(ids)
        texts = np.concatenate(texts)
        ret = pd.DataFrame()
        if system_data:
            ret["__truera_id__"] = ids
        ret["text"] = texts
        if extra_data and self._base_data_split.extra_data_df is not None:
            df = self._base_data_split.extra_data_df
            df = df.set_index("__truera_id__")
            df = df.loc[ids]
            df.index = ret.index
            ret = pd.concat([ret, df], axis=1)
        return ret

    @cached(cache=LRUCache(maxsize=16))
    def get_ys(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False,
        batch_size: int = 4
    ) -> Union[pd.Series, pd.DataFrame]:
        tru_batches = self._get_batches(
            start=start, stop=stop, batch_size=batch_size, batch_type="tru"
        )
        if system_data:
            ret = [
                pd.DataFrame({
                    "__truera_id__": curr.ids,
                    "label": curr.labels
                }) for curr in tru_batches
            ]
        else:
            ret = [pd.Series(curr.labels) for curr in tru_batches]
        ret = pd.concat(ret)
        return ret

    def _get_ys_pred_raw(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        batch_size: int = 4,
    ) -> Tuple[np.ndarray, np.ndarray]:
        from trulens.nn.models import discern_backend

        # Static methods only but we create instance anyway to simplify typing hints.
        model_load_wrapper = self._model.model_obj
        from_text_model_run_wrapper = self._model.model_run_wrapper

        model = model_load_wrapper.get_model()
        tokenizer = model_load_wrapper.get_tokenizer(
            from_text_model_run_wrapper.n_tokens
        )

        self._logger.debug('Loaded model and tokenizer.')
        backend = discern_backend(model)
        os.environ['TRULENS_BACKEND'] = backend.name.lower()
        model_run_wrapper = self._model.model_run_wrapper

        ids = []
        preds = []
        data_batches = self._get_batches(
            start=start, stop=stop, batch_size=batch_size, batch_type="data"
        )
        for data_batch in data_batches:
            batched_ids, batched_preds = self._get_batched_ys_pred_raw(
                data_batch,
                model=model,
                model_wrapper=model_run_wrapper,
                model_config=self._attr_config,
                tokenizer_wrapper=tokenizer,
                from_text_model_run_wrapper=from_text_model_run_wrapper,
            )
            ids.append(batched_ids)
            preds.append(batched_preds)
        ids = np.concatenate(ids)
        preds = np.concatenate(preds)
        return ids, preds

    def _get_batched_ys_pred_raw(
        self,
        ds_batch: Any,
        *,
        model: NNB.Model,
        model_wrapper: base.Wrappers.ModelRunWrapper,
        model_config: AttributionConfiguration,
        tokenizer_wrapper: Optional[nlp.Wrappers.TokenizerWrapper] = None,
        from_text_model_run_wrapper: Optional[nlp.Wrappers.ModelRunWrapper
                                             ] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        import trulens.nn.backend as B

        assert isinstance(
            model_wrapper, nlp.Wrappers.ModelRunWrapper
        ), "ModelRunWrapper used does not inherit from nlp.Wrappers.ModelRunWrapper"

        tru_data: nlp.Types.TruBatch = model_wrapper.trubatch_of_databatch(
            ds_batch, model=model, tokenizer=tokenizer_wrapper
        )
        if from_text_model_run_wrapper is not None:
            text_data: nlp.Types.TextBatch = model_wrapper.textbatch_of_trubatch(
                tru_data
            )
            # first create input batches
            inputbatch: nlp.Wrappers.Types.InputBatch = from_text_model_run_wrapper.inputbatch_of_textbatch(
                texts=list(text_data), model=model, tokenizer=tokenizer_wrapper
            )

            # Evaluating model in smaller batches than data has come in.
            batch_preds = inputbatch.map_batch(
                lambda batch: from_text_model_run_wrapper.
                evaluate_model(model, batch).probits,
                batch_size=model_config.rebatch_size
            )

        else:
            # TODO(corey): Doesn't this need to be probits?
            inputbatch = model_wrapper.inputbatch_of_databatch(ds_batch, model)
            batch_preds = model_wrapper.evaluate_model(model, inputbatch)

        # convert to np if neccessary
        if not isinstance(
            batch_preds, np.ndarray
        ) and len(batch_preds) > 0 and not isinstance(batch_preds[0], str):
            batch_preds = B.get_backend().as_array(batch_preds)
        return tru_data.ids, batch_preds

    @cached(cache=LRUCache(maxsize=16))
    def get_ys_pred(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False,
        wait: bool = True,
        batch_size: int = 4
    ) -> Union[pd.Series, pd.DataFrame]:
        if not wait:
            raise ValueError("For local computations `wait` must be `True`!")
        ids, ys_preds = self._get_ys_pred_raw(
            start=start, stop=stop, batch_size=batch_size
        )
        if self._get_score_type() == "logits":
            ys_preds = logit(ys_preds)
        elif self._get_score_type() == "classification":
            if len(
                ys_preds.shape
            ) == 1 or (len(ys_preds.shape) == 2 and ys_preds.shape[1] == 1):
                # Assume binary classification.
                ys_preds = (ys_preds > 0.5).astype(int)
            else:
                # Assume `ys_preds.shape[1]` classes.
                ys_preds = np.argmax(ys_preds, axis=1)
        ret = pd.DataFrame()
        if system_data:
            ret["__truera_id__"] = ids
        ret = pd.concat([ret, pd.DataFrame(ys_preds)], axis=1)
        if ret.shape[1] == 1:
            return ret.iloc[:, 0]
        return ret

    def get_feature_influences_for_data(self):
        pass

    def get_influences_background_data_split_or_set_from_default(self):
        return self._data_collection.data_splits[self._base_data_split.name]

    def set_base_data_split(self, data_split_name: str):
        from truera.rnn.general.container.artifacts import ArtifactsContainer
        from truera.rnn.general.service.container import Locator
        from truera.rnn.general.service.sync_service import SyncService
        if data_split_name not in self._data_collection.data_splits:
            raise ValueError(f"No such data split \"{data_split_name}\"!")
        cache_dir = self._explanation_cache.get_temp_dir(
            project_name=self._project.name,
            model_name=self._model.name,
            data_collection_name=self._data_collection.name,
            data_split_name=data_split_name,
            hash_bg=DEFAULT_NN_HASH_BG,
            score_type=self._get_score_type(),
            algorithm=ExplanationAlgorithmType.INTEGRATED_GRADIENTS
        )

        # pylint: disable=not-callable
        self.sync_client = SyncService(
            cache_dir.name,
            needs_local_proxy_cache=False,
            local_workspace_mode=True
        )
        self._artifacts_container = ArtifactsContainer(
            self.sync_client,
            locator=Locator.Artifact(
                self._project.name, self._model.name,
                self._data_collection.name, data_split_name
            )
        )

        artifact_split_counterfactual = data_split_name + '_counterfactual'
        self._artifacts_container_cf = ArtifactsContainer(
            self.sync_client,
            locator=Locator.Artifact(
                self._project.name, self._model.name,
                self._data_collection.name, artifact_split_counterfactual
            )
        )

        #TODO: add artifacts locator to interact with other segments
        self._base_data_split = self._data_collection.data_splits[
            data_split_name]

    def global_token_summary(
        self,
        token_type: str = None,
        num_records: int = None,
        max_words_to_track: int = 500,
        offset: int = 0
    ):
        """ Summary and exploration of the most important tokens in the split.

        Args:
            token_type: The tokenization to show, can be 'token' or 'word'. Defaults to 'word' if words were ingested, otherwise 'token'.
            num_records: The number of records to use.
            max_words_to_track: The maximum number of words to show. Defaults to 500.
            offset: An index offset for the records to use. Defaults to 0.

        Returns:
            An interactive widget.
        """
        from truera.nlp.general.aiq.visualizations import Figures

        # Generate data if not already there
        self.get_feature_influences(token_type="token")
        token_type_enum = self._check_valid_token_type(token_type)

        viz = Figures(self._aiq)

        return viz.global_token_summary(
            artifacts_container=self._artifacts_container,
            num_records=num_records,
            max_words_to_track=max_words_to_track,
            offset=offset,
            token_type=token_type_enum,
        )

    def record_explanations_attribution_tab(
        self, token_type: str = None, num_records: int = None
    ):
        """ Display the influence profile plot and feature interactions of each sentence in the split.

        Args:
            token_type: The tokenization to show, can be 'token' or 'word'. Defaults to 'word' if words were ingested, otherwise 'token'.
            num_records: The number of records to use.

        Returns:
            An interactive widget.
        """

        from truera.nlp.general.aiq.visualizations import Figures

        # Generate data if not already there
        self.get_feature_influences(token_type="token")
        token_type_enum = self._check_valid_token_type(token_type)

        viz = Figures(self._aiq)

        return viz.record_explanations_attribution_tab(
            artifacts_container=self._artifacts_container,
            num_records=num_records,
            token_type=token_type_enum,
        )

    def data_exploration_tab(
        self,
        token_type: str = None,
        num_records: int = None,
        max_influence_examples_per_token: int = 10,
        num_train_examples_per_token: int = 5,
        max_words_to_track: int = 500,
        offset: int = 0
    ):
        """ Explore split data per token.

        Args:
            token_type: The tokenization to show, can be 'token' or 'word'. Defaults to 'word' if words were ingested, otherwise 'token'.
            num_records: The number of records to use.
            max_influence_examples_per_token: The maximum number of examples to show with influences. Defaults to 10.
            num_train_examples_per_token: The maximum number of examples to show. Defaults to 5.
            max_words_to_track: The maximum number of words to show. Defaults to 500.
            offset: An index offset for the records to use. Defaults to 0.

        Returns:
            An interactive widget.
        """

        from truera.nlp.general.aiq.visualizations import Figures

        # Generate data if not already there
        self.get_feature_influences(token_type="token")
        token_type_enum = self._check_valid_token_type(token_type)
        viz = Figures(self._aiq)

        return viz.data_exploration_tab(
            artifacts_container=self._artifacts_container,
            num_records=num_records,
            max_influence_examples_per_token=max_influence_examples_per_token,
            num_train_examples_per_token=num_train_examples_per_token,
            max_words_to_track=max_words_to_track,
            offset=offset,
            token_type=token_type_enum
        )

    def model_robustness_analysis_tab(self, token_type: str = None) -> None:
        """ Explore how your model may change it's outputs with token swaps.

        Args:
            token_type: The tokenization to show, can be 'token' or 'word'. Defaults to 'word' if words were ingested, otherwise 'token'.

        Returns:
            An interactive widget.
        """

        from truera.nlp.general.aiq.visualizations import Figures
        self.get_feature_influences(token_type="token")

        self.get_feature_influences(
            compute_counterfactuals=True, token_type="token"
        )
        token_type_enum = self._check_valid_token_type(token_type)

        viz = Figures(self._aiq)

        return viz.model_robustness_analysis_tab(
            self._artifacts_container,
            self._artifacts_container_cf,
            token_type=token_type_enum
        )

    def token_influence_comparison_tab(
        self, max_words_to_track: int = 500, token_type: str = None
    ) -> None:
        """ Compare influence profiles between two tokens. This helps see how tokens differ.

        Args:
            max_words_to_track: The maximum number of words to show. Defaults to 500.
            token_type: The tokenization to show, can be 'token' or 'word'. Defaults to 'word' if words were ingested, otherwise 'token'.
            
        Returns:
            An interactive widget.
        """

        from truera.nlp.general.aiq.visualizations import Figures

        # Generate data if not already there
        self.get_feature_influences(token_type="token")
        token_type_enum = self._check_valid_token_type(token_type)

        viz = Figures(self._aiq)

        return viz.token_influence_comparison(
            self._artifacts_container,
            token_type=token_type_enum,
            max_words_to_track=max_words_to_track
        )

    def evaluate_text_tab(self,) -> None:
        """
        Evaluate new text to test hypothesis.
        """
        from truera.nlp.general.aiq.visualizations import Figures

        # Generate data if not already there
        self.get_feature_influences()
        viz = Figures(self._aiq)
        model_load_wrapper = self._model.model_obj
        if self._virtual_model_breakage_check(
            breakage_message="the evaluate_text_tab widget will be unavailable"
        ):
            return
        model = model_load_wrapper.get_model()
        model_run_wrapper = self._model.model_run_wrapper
        tokenizer = model_load_wrapper.get_tokenizer(model_run_wrapper.n_tokens)

        return viz.evaluate_text_tab(
            self._artifacts_container, model_run_wrapper, model, tokenizer
        )

    def _ensure_data_split(self):
        pass

    def set_comparison_data_splits(self):
        pass

    def get_base_data_split(self):
        pass

    def get_data_collection(self) -> str:
        return self._data_collection.name

    def get_comparison_data_splits(self):
        pass

    def set_segment(self, segment_group_name: str, segment_name: str):
        pass

    def clear_segment(self):
        pass

    def compute_performance(
        self,
        metric_type: Optional[str] = None,
        threshold: float = 0.5,
        plot_roc: bool = False
    ) -> Dict[str, Union[float, Dict[int, float]]]:
        """
        Wrapper function for Explainer._compute_performance(). Computes various
        metrics on the label and predictions. To see the list of available
        metrics, use list_performance_metrics .

        Args:
            - metric_type (str): The metric to calculate from
              list_performance_metrics. If None, it will calculate all metrics.
            - threshold (float): The classification threshold to convert probas.
              Default is 0.5.
            - plot_roc (bool): a flag on whether to plot the roc curve.

        Returns:
            - dict: A dict of metric names to metric values
        """
        ys = self.get_ys()
        ys_preds = self.get_ys_pred().to_numpy()
        return self._compute_performance(
            ys, ys_preds, metric_type, threshold, plot_roc
        )

    def get_all_computed_feature_influences(
        self
    ) -> Mapping[ExplainerQiiCacheKey, pd.DataFrame]:
        self._qiis = self.get_feature_influences()
        if self._qiis is None:
            return {}

        return {
            ExplainerQiiCacheKey(
                self._get_score_type(), ExplanationAlgorithmType.INTEGRATED_GRADIENTS
            ):
                self._qiis
        }

    def get_feature_influences(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        score_type: Optional[str] = None,  # this is unused for now
        batch_size: int = 2,
        token_type: str = None,
        force_compute: bool = False,
        compute_counterfactuals: bool = False
    ) -> pd.DataFrame:
        """
        Gets the input influences.

        Args:
            - start (int): A starting offset of the data records
            - stop (int): A stop offset of the data records
            - batch_size (int): The number of records in a influence
              calculation. This parameter is used to modify for speed vs memory
              constraints.
            - token_type (str): the token aggregation type to return. Can be "word" or
              "token". Both types will try to be generated irregardless of this parameter.
            - force_compute (bool): A flag to recompute influences even if
              already calculated
            - compute_counterfactuals (bool): A flag to calculate counterfactual
              influences. If original influences are not availablem it will also
              calculate those.
        Returns:
            - pd.DataFrame: a dataframe of the original sentence, and influences
              per specified TokenType
        """
        stop_requested = stop is not None
        start, stop = self._convert_start_stop(start, stop, metrics_count=False)
        from truera.client.local.intelligence.nlp_explainer_util import \
            _generate_feature_influences
        from truera.client.local.intelligence.nlp_explainer_util import \
            _get_feature_influences_from_cache

        if token_type is None:
            model_load_wrapper = self._model.model_obj
            from_text_model_run_wrapper = self._model.model_run_wrapper
            if model_load_wrapper == ModelType.VIRTUAL:
                if self._aiq.model.has_words(self._artifacts_container):
                    self._logger.info(
                        "token_type not supplied. Assuming token_type 'word' since word artifacts were found."
                    )
                    token_type = "word"
                else:
                    self._logger.info(
                        "token_type not supplied. Assuming token_type 'token' since word artifacts were not found."
                    )
                    token_type = "token"
            else:
                tokenizer = model_load_wrapper.get_tokenizer(
                    from_text_model_run_wrapper.n_tokens
                )
                if tokenizer.has_tokenspans:
                    self._logger.info(
                        "token_type not supplied. Assuming token_type 'word' since spans are supplied."
                    )
                    token_type = "word"
                else:
                    self._logger.info(
                        "token_type not supplied. Assuming token_type 'token' since spans are not supplied."
                    )
                    token_type = "token"
        token_type = self._token_type.from_str(token_type)

        influences, output_path_original = _get_feature_influences_from_cache(
            self, self._artifacts_container, stop, token_type=token_type
        )

        if force_compute or influences is None or (
            stop_requested and influences.shape[0] < stop
        ):
            if stop > self._attr_config.n_metrics_records:
                raise ValueError(
                    f"stop={stop} cannot be greater than {self._attr_config.__class__.__name__}.n_metrics_records={self._attr_config.n_metrics_records}"
                )

            if not self._virtual_model_breakage_check(
                breakage_message="influence generation will be skipped"
            ):
                influences = _generate_feature_influences(
                    self,
                    start=start,
                    stop=stop,
                    batch_size=batch_size,
                    token_type=token_type,
                    is_counterfactuals=False
                )
        if compute_counterfactuals:
            influences_cf, output_path_cf = _get_feature_influences_from_cache(
                self, self._artifacts_container_cf, stop, token_type=token_type
            )
            temp_cf_generated_check = os.path.exists(
                output_path_cf / 'original_ids.dat'
            )
            # Temporarily using a different CF check since we de-activated counterfactual influences
            # See MLNN-177
            if force_compute or not temp_cf_generated_check:  #influences_cf is None:
                from truera.client.nn.wrappers.torch import Torch
                from truera.nlp.general.model_runner_proxy.nlp_counterfactuals import \
                    calculate_counterfactual
                self._logger.info("Generating Counterfactuals.")
                calculate_counterfactual(
                    self._aiq, self._artifacts_container, output_path_cf,
                    Torch.get_device()
                )
                num_counterfactuals_multiplier = 1
                stop_cf = (len(influences)) * num_counterfactuals_multiplier

                if not self._virtual_model_breakage_check(
                    breakage_message="counterfactual generation will be skipped"
                ):
                    influences_cf = _generate_feature_influences(
                        self,
                        stop=stop_cf,
                        batch_size=batch_size,
                        token_type=token_type,
                        is_counterfactuals=True
                    )
                    return influences_cf[start:stop]

        return influences[start:stop]

    def get_cache_dir_path(self) -> str:
        return self.sync_client.local_cache_path
