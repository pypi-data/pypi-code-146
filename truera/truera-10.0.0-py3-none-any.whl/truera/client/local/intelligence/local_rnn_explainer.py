import csv
import json
import logging
import os
from pathlib import Path
import tempfile
from typing import Dict, Mapping, Optional, Sequence, Tuple, Union
import warnings

import numpy as np
import pandas as pd
import yaml

from truera.client.intelligence.explainer import NonTabularExplainer
from truera.client.local.local_artifacts import Cache
from truera.client.local.local_artifacts import DataCollection
from truera.client.local.local_artifacts import Model
from truera.client.local.local_artifacts import Project
from truera.client.nn.client_configs import RNNAttributionConfiguration
from truera.client.nn.wrappers.datasets import convert_to_truera_iterable
from truera.client.nn.wrappers.timeseries import Wrappers as Timeseries
from truera.client.truera_workspace_utils import ExplainerQiiCacheKey
from truera.protobuf.public.qoi_pb2 import \
    ExplanationAlgorithmType  # pylint: disable=no-name-in-module

warnings.filterwarnings("ignore")

DASH_PORT = 12345
SUPPORTED_QOI = [
    "average", "last", "timestep", "first default (ground_truth)",
    "first default (prediction)"
]
SUPPORTED_LAYER_NAME = ["input", "internal"]


class LocalRNNExplainer(NonTabularExplainer):
    _NUM_DEFAULT_INFLUENCES = 100

    def __init__(
        self, model: Model, data_collection: DataCollection, data_split: str,
        project: Project, attr_config: RNNAttributionConfiguration,
        explanation_cache: Cache, logger: logging.Logger
    ) -> None:
        # TODO: these imports are put inside the class init for now since they depend on rnn extras being installed
        from jupyter_dash import JupyterDash

        from truera.client.intelligence.interactions.interaction_explainer import \
            InteractionExplainer
        from truera.rnn.general.aiq.aiq import RnnAIQ
        from truera.rnn.general.aiq.visualizations import Figures
        from truera.rnn.general.container.rnnmodel import RNNModelProxy
        from truera.rnn.general.selection.interaction_selection import \
            ModelGrouping

        super().__init__(
            model=model,
            data_collection=data_collection,
            data_split=data_split,
            project=project,
            attr_config=attr_config,
            explanation_cache=explanation_cache,
            logger=logger
        )

        self._InteractionExplainer = InteractionExplainer
        self.GROUPING_OPTION_TO_STR = ModelGrouping.option_to_label()
        self.STR_TO_GROUPING_OPTION = {
            "".join(self.GROUPING_OPTION_TO_STR[i].lower().split()): i
            for i in self.GROUPING_OPTION_TO_STR
        }

        self._base_data_split = None
        self._qiis = None
        self._feature_names_to_idx = {}
        self.set_base_data_split(data_split)

        # Intelligence API - related inits
        self._model_proxy = RNNModelProxy()
        self._aiq = RnnAIQ(self._model_proxy)
        self._figures = Figures(self._aiq)
        self._app = JupyterDash("local_viz")

    def _get_output_classes(self) -> int:
        return self._attr_config.n_output_neurons

    def _get_score_type(self) -> str:
        return self._project.score_type

    def _load_data_from_cache(self, cache_dir: tempfile.TemporaryDirectory):
        if not os.path.exists(
            os.path.join(
                cache_dir.name, self._base_data_split.name,
                "input_attrs_per_timestep.dat"
            )
        ):
            return
        xs_shape = np.load(
            os.path.join(
                self._artifacts_container.get_path(), "data_shape.npy"
            )
        )
        self._input_lengths = np.concatenate(
            self._model_proxy.get_lengths(
                self._artifacts_container, xs_shape[0]
            )
        )
        self._base_data_split.xs_pre = self._aiq.get_data(
            self._artifacts_container, len(self._input_lengths)
        )
        num_records = len(self._base_data_split.xs_pre)
        self._qiis = self._aiq.get_influences_per_timestep(
            "input", self._artifacts_container, num_records
        )

        self._ys = self._aiq.get_ground_truth(
            self._artifacts_container, num_records
        )
        self._ys_pred = self._aiq.get_predictions(
            self._artifacts_container, num_records
        )

        feature_names = next(
            csv.reader(
                open(
                    os.path.join(
                        cache_dir.name, self._base_data_split.name,
                        "feature_names.csv"
                    ), "r"
                ),
                delimiter=","
            )
        )
        self._feature_names_to_idx = {
            feature_names[i]: i for i in range(len(feature_names))
        }

    def get_feature_names(self):
        return self._base_data_split.truera_wrappers.split_load_wrapper.get_feature_names(
        )

    def get_interaction_explainer(self):
        """
        Gets a class that has interaction workflows

        Returns:
            InteractionExplainer: A class with interaction workflow APIs
        """
        return self._InteractionExplainer(self._aiq, self._artifacts_container)

    def _check_feature_exists(self, feature):
        canonicalized_feature = feature.lower()
        canonicalized_feature_names = [
            name.lower() for name in self.get_feature_names()
        ]
        if not canonicalized_feature in canonicalized_feature_names:
            raise ValueError(f"Feature {feature} does not exist!")

    def _get_feature_transform_map(self):
        artifacts_cache_dir = Path(
            self.sync_client.get_cache_path(self._artifacts_container.locator)
        )
        feature_names = self.get_feature_names()
        feature_transform_path = os.path.join(
            artifacts_cache_dir.resolve(), "feature_transform_map.json"
        )
        if not os.path.exists(feature_transform_path):
            feature_map = []
        else:
            with open(feature_transform_path, "r") as json_file:
                raw_feature_map = json.load(json_file)
            # maps preprocessed col index -> list of postprocessed col indices
            feature_map = []
            postprocessed_cols = 0
            for f in feature_names:
                num_cols = raw_feature_map.get(f, 1)
                feature_map.append(
                    list(
                        range(
                            postprocessed_cols, postprocessed_cols + num_cols
                        )
                    )
                )
                postprocessed_cols += num_cols
        return feature_map

    def get_xs(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        extra_data: bool = False,
        system_data: bool = False
    ) -> np.ndarray:
        start, stop = self._convert_start_stop(start, stop)
        data = self._base_data_split.xs_pre
        if isinstance(data, pd.DataFrame):
            return data.iloc[start:stop, :]
        elif isinstance(data, np.ndarray):
            return data[start:stop, :]
        raise TypeError(
            f"Data must be of type pandas.DataFrame or numpy.ndarray. Found {type(data)}."
        )

    def extract_feature_splines(
        self,
        num_records: Optional[int] = None,
        length_thresh: Optional[int] = None,
        length_thresh_le: bool = False,
        qoi_core_class: int = 0,
        qoi_compare_class: int = 0,
        qoi: str = "last",
        qoi_timestep: int = 0,
        pred_thresh: float = 0.5,
        poly_order: int = 3
    ) -> np.ndarray:
        """
        Gets the feature splines of input attributions.
        Args:
            num_records (int or None): The number of records to return. If none, will return all.
            length_thresh (int or None): An optional filter on record timeseries length.
            length_thresh_le (bool): A flag for the length threshold filter being less than or greater than. Defaults to False.
            qoi_core_class (int): The main class to get influences from.
            qoi_compare_class (int): A comparitive class to subtract from the main qoi_core_class. This gets a difference of classes explanation.
            qoi (str): The type of qoi. Options are ["last", "average","timestep","first default (prediction), "first default (ground truth)"]. These reference the timestep outputs.
            qoi_timestep (int): If the qoi is "timestep", this helps specify the timestep output
            pred_thresh (float): A threshold to use for filters. Defaults to 0.5
            poly_order (int): The polynomial order for splines. Defaults to 3

        Returns:
            spline_coefficients (np.ndarray): An array of spline coefficients. The dimensions will be (feature_id x timestep x polynomial order). Splines can be loaded in python with:
                spline_f = np.poly1d(spline_coefficients[feature_idx][timestep]) 
                extracted_feature += spline_f(data[feature_idx][timestep])
        """

        # Generate data if not already there
        self.get_feature_influences()
        num_records = min(num_records,
                          len(self._qiis)) if num_records else len(self._qiis)
        return self._aiq.feature_splines_export_info(
            self._artifacts_container,
            num_records,
            length_thresh=length_thresh,
            length_thresh_le=length_thresh_le,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            poly_order=poly_order
        )

    def compute_performance(
        self,
        metric_type: Optional[str] = None,
        output_class: int = 0,
        output_time_step: Optional[int] = None,
        threshold: float = 0.5,
        plot_roc: bool = False
    ) -> Dict[str, Union[float, Dict[int, float]]]:
        """
        Wrapper function for Explainer._compute_performance(). Computes various metrics on the label and predictions. To see the list of available metrics, use list_performance_metrics

        Args:
            metric_type (str): The metric to calculate from list_performance_metrics. If None, it will calculate all metrics. 
            output_class (int): The class index to check metrics against. The default is class 0.
            output_time_step (int or None): The output timestep to check metrics against. If None, all timesteps will be used. 
            threshold (float): The classification threshold to convert probas. Default is 0.5.
            plot_roc (bool): a flag on whether to plot the roc curve.

        Returns:
            dict: A dict of metric names to metric values
        """
        ys = self.get_ys(
            output_class=output_class, output_time_step=output_time_step
        )
        ys_preds = self.get_ys_pred(
            output_class=output_class, output_time_step=output_time_step
        )
        return self._compute_performance(
            ys, ys_preds, metric_type, threshold, plot_roc
        )

    def _get_label_like(
        self,
        cache_data: np.ndarray,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        output_class: int = 0,
        output_time_step: Optional[int] = None
    ) -> np.ndarray:
        _, timestep_dim_size, class_dim_size = cache_data.shape
        if output_class > class_dim_size or output_class < 0:
            raise ValueError(
                f"Output class supplied:{output_class} must be between 0 and the total number of classes: {class_dim_size}"
            )
        cache_data = cache_data[start:stop, :, output_class]
        if output_time_step is None:
            label_like_filtered = cache_data.flatten()
        else:
            if output_time_step > timestep_dim_size or output_time_step < 0:
                raise ValueError(
                    f"Output time step supplied: {output_time_step} must be between 0 and the total number of output time steps: {timestep_dim_size}"
                )
            label_like_filtered = cache_data[:, output_time_step]
        return label_like_filtered

    def get_ys(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False,
        output_class: int = 0,
        output_time_step: Optional[int] = None
    ) -> Union[pd.Series, pd.DataFrame]:
        # TODO: separate influences cache from non influence caches in get_feature_influences
        start, stop = self._convert_start_stop(start, stop)
        self.get_feature_influences(start=start, stop=stop)
        ys = self._get_label_like(
            self._ys,
            start=start,
            stop=stop,
            output_class=output_class,
            output_time_step=output_time_step
        )
        if len(ys.shape) == 2 and ys.shape[1] > 1:
            ret = pd.DataFrame(ys)
        else:
            ret = pd.DataFrame(ys.ravel())
        if system_data:
            # This is a hack till we use data layer.
            ret["__truera_id__"] = list(range(ret.shape[0]))
        if ret.shape[1] == 1:
            ret = ret.iloc[:, 0]
        return ret

    def get_ys_pred(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        output_class: int = 0,
        output_time_step: Optional[int] = None
    ) -> Union[pd.Series, pd.DataFrame]:
        # TODO: separate influences cache from non influence caches in get_feature_influences
        start, stop = self._convert_start_stop(start, stop)
        self.get_feature_influences(start=start, stop=stop)
        ret = self._get_label_like(
            self._ys_pred,
            start=start,
            stop=stop,
            output_class=output_class,
            output_time_step=output_time_step
        )
        if len(ret.shape) == 1:
            ret = pd.Series(ret)
        else:
            ret = pd.DataFrame(ret)
        return ret

    def get_feature_influences_for_data(
        self,
        pre_data: pd.DataFrame,
        post_data: Optional[pd.DataFrame] = None,
        ys: Optional[Union[np.ndarray, pd.Series]] = None,
        score_type: Optional[str] = None,
        comparison_post_data: Optional[pd.DataFrame] = None,
        num_internal_qii_samples: int = 1000,
        algorithm: str = "truera-qii"
    ) -> pd.DataFrame:
        raise NotImplementedError(
            "This functionality is not implemented for RNN explainers!"
        )

    def get_feature_influences(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        score_type: Optional[str] = None,  # this is unused for now
        force_compute: bool = False,
        shuffle_data: bool = False,
        algorithm: str = "truera-ig",  # this is unused for now,
        compute_interactions: bool = True,
    ) -> pd.DataFrame:
        """
        Computes feature influence artifacts and saves them in a temp directory. To save permanently or to use remote features, you will need to upload via tru.upload()

        Args:
            start (int or None): start index of data to compute. defaults to 0
            stop (int or None): end index of data to compute. defaults to the explainer default.
            score_type (str or None): Unused for now. The score type. ex) classification, regression, logit, probit
            force_compute (bool): a force flag to recompute. otherwise, if cache results are available, then the cache will be returned.
            shuffle_data (bool): a flag to shuffle the incoming data
            algorithm (str): Unused for now. The explanation algorithm.
            compute_interactions (bool): A flag to compute interaction artifacts. These are needed for the InteractionExplainer.
            

        Returns:
            pd.DataFrame: the feature influences
        """
        start, stop = self._convert_start_stop(start, stop, metrics_count=False)
        output_tempdir = self._explanation_cache.get_temp_dir(
            project_name=self._project.name,
            model_name=self._model.name,
            data_collection_name=self._data_collection.name,
            data_split_name=self._base_data_split.name,
            hash_bg=self._attr_config.baseline_split,
            score_type=self._get_score_type(),
            algorithm=ExplanationAlgorithmType.INTEGRATED_GRADIENTS
        )
        if self._qiis is None:
            self._load_data_from_cache(output_tempdir)
        if self._qiis is not None:
            if not force_compute:
                return self._qiis[start:stop, :]
        attr_config = self._attr_config
        if attr_config.baseline_split not in self._data_collection.data_splits:
            raise ValueError(f"The baseline split defined in RNNAttributionConfiguration does not exist: {attr_config.baseline_split}. "\
                "Please add this split to the project")
        self._logger.info("Calculating feature influences")

        from truera.rnn.general.model_runner_proxy.baseline_utils import \
            BaselineConstructor
        from truera.rnn.general.model_runner_proxy.mem_utils import \
            save_rnn_model_info
        from truera.rnn.general.model_runner_proxy.rnn_attributions import \
            RNNAttribution
        from truera.rnn.general.model_runner_proxy.sampling_utils import \
            prepare_datasplit
        if isinstance(self._model.model_obj, Timeseries.ModelLoadWrapper):
            model = self._model.model_obj.get_model()
        else:
            model = self._model.model_obj
        baseline_split = self._data_collection.data_splits[
            attr_config.baseline_split]
        from trulens.nn.models import discern_backend
        backend = discern_backend(model)
        n_baseline_records = attr_config.n_baseline_records
        n_explain_records = stop
        batch_size = 64
        baseline_ds, batch_size, is_unknown_ds_type = prepare_datasplit(
            convert_to_truera_iterable(
                baseline_split.truera_wrappers.split_load_wrapper.get_ds()
            ),
            backend=backend,
            batch_size=batch_size,
            model=model,
            model_wrapper=self._model.model_run_wrapper,
            num_take_records=n_baseline_records,
            shuffle=shuffle_data
        )

        baseline_constructor = BaselineConstructor(
            baseline_ds,
            baseline_split.truera_wrappers.split_load_wrapper.get_data_path(),
            model, self._base_data_split.truera_wrappers.split_load_wrapper,
            self._model.model_run_wrapper, attr_config, batch_size
        )  # this fn needs model_name and n_time_step from attr_config
        batched_baseline = baseline_constructor.construct_avg_baseline()

        artifacts_cache = Path(
            self.sync_client.get_cache_path(self._artifacts_container.locator)
        )
        artifacts_cache.mkdir(parents=True, exist_ok=True)

        self._logger.info(f"Output path: {artifacts_cache.resolve()}")
        feature_names = self.get_feature_names()
        with open(
            os.path.join(artifacts_cache.resolve(), "feature_names.csv"),
            "w+",
            newline=""
        ) as feature_file:
            wr = csv.writer(feature_file, quoting=csv.QUOTE_ALL)
            wr.writerow(feature_names)

        with open(
            os.path.join(artifacts_cache.resolve(), "feature_dict.json"), "w"
        ) as short_desc_fp:
            json.dump(
                self._base_data_split.truera_wrappers.split_load_wrapper.
                get_short_feature_descriptions(), short_desc_fp
            )
        self._logger.info("Feature name artifacts copied to output path.")

        # save run config
        run_config = {
            "n_baseline_records": n_baseline_records,
            "n_explain_records": n_explain_records,
            "shuffle_data": shuffle_data,
            "batch_size": batch_size
        }
        with open(
            os.path.join(artifacts_cache.resolve(), "run_config.yaml"), "w"
        ) as f:
            yaml.dump(run_config, f)

        metrics_ds, _, _ = prepare_datasplit(
            convert_to_truera_iterable(
                self._base_data_split.truera_wrappers.split_load_wrapper.get_ds(
                )
            ),
            backend=backend,
            batch_size=batch_size,
            model=model,
            model_wrapper=self._model.model_run_wrapper,
            shuffle=shuffle_data
        )
        split_ds, _, _ = prepare_datasplit(
            convert_to_truera_iterable(
                self._base_data_split.truera_wrappers.split_load_wrapper.get_ds(
                )
            ),
            backend=backend,
            batch_size=batch_size,
            model=model,
            model_wrapper=self._model.model_run_wrapper,
            shuffle=shuffle_data
        )
        self._logger.info("=== Step 2/5: Save Model Info ===")
        sample_size = n_explain_records
        metrics_size = n_explain_records
        save_rnn_model_info(
            metrics_ds,
            model,
            self._model.model_run_wrapper,
            self._base_data_split.truera_wrappers.split_load_wrapper,
            metrics_size,
            sample_size,
            artifacts_cache.resolve(),
            attr_config,  # need n_time_step and n_time_step_output
            backend,
            forward_padded=attr_config.forward_padded
        )

        self._logger.info("=== Step 3/5: Input Attributions ===")
        filter_func = None
        rnn_attributor = RNNAttribution()
        total_records, total_iterations = rnn_attributor.count_records(
            split_ds,
            self._model.model_run_wrapper,
            model,
            n_explain_records,
            backend,
            filter_func=filter_func,
            return_iterations=True
        )
        if (is_unknown_ds_type):
            # unknown iterable types may not refresh dataset from the beginning
            split_ds, _, _ = prepare_datasplit(
                convert_to_truera_iterable(
                    self._base_data_split.truera_wrappers.split_load_wrapper.
                    get_ds()
                ),
                backend=backend,
                batch_size=batch_size,
                model=model,
                model_wrapper=self._model.model_run_wrapper,
                shuffle=shuffle_data
            )

        rnn_attributor.calculate_attribution_per_timestep(
            split_ds,
            self._model.model_run_wrapper,
            model,
            batched_baseline,
            artifacts_cache.resolve(),
            total_records,
            attr_config,  # need args: n_time_step, n_time_step_output, n_features, output_layer, input_layer, num_classes, 
            backend,
            filter_func=filter_func,
            input_anchor=attr_config.input_anchor,
            output_anchor=attr_config.output_anchor,
            max_iterations=total_iterations,
            compute_interactions=compute_interactions
        )

        self._load_data_from_cache(
            output_tempdir
        )  # result is stored  as files in cache. need to load it to self._qiis
        return self._qiis[start:stop, :]

    def set_base_data_split(self, data_split_name: str):
        if data_split_name not in self._data_collection.data_splits:
            raise ValueError(f"No such data split \"{data_split_name}\"!")
        from truera.rnn.general.container.artifacts import ArtifactsContainer
        from truera.rnn.general.service.container import Locator
        from truera.rnn.general.service.sync_service import SyncService
        cache_dir = self._explanation_cache.get_temp_dir(
            project_name=self._project.name,
            model_name=self._model.name,
            data_collection_name=self._data_collection.name,
            data_split_name=data_split_name,
            hash_bg=self._attr_config.baseline_split,
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
        self._base_data_split = self._data_collection.data_splits[
            data_split_name]

    def _ensure_data_split(self):
        raise NotImplementedError(
            "This functionality is not implemented for RNN explainers!"
        )

    def set_comparison_data_splits(
        self,
        comparison_data_splits: Optional[Sequence[str]] = None,
        use_all_data_splits: bool = False
    ):
        raise NotImplementedError(
            "This functionality is not implemented for RNN explainers!"
        )

    def get_base_data_split(self) -> str:
        raise NotImplementedError(
            "This functionality is not implemented for RNN explainers!"
        )

    def get_data_collection(self) -> str:
        return self._data_collection.name

    def get_comparison_data_splits(self) -> Sequence[str]:
        raise NotImplementedError(
            "This functionality is not implemented for RNN explainers!"
        )

    def get_influences_background_data_split_or_set_from_default(self):
        return self._data_collection.data_splits[
            self._attr_config.baseline_split]

    def compute_feature_contributors_to_instability(
        self,
        score_type: Optional[str] = None,
        use_difference_of_means: bool = False
    ) -> pd.DataFrame:
        raise NotImplementedError(
            "This functionality is not implemented for RNN explainers!"
        )

    def compute_estimated_performance(self,
                                      metric_type: str) -> Tuple[float, str]:
        raise NotImplementedError(
            "This functionality is not implemented for RNN explainers!"
        )

    def set_segment(self, segment_group_name: str, segment_name: str):
        raise NotImplementedError(
            "This functionality is not implemented for RNN explainers!"
        )

    def clear_segment(self):
        raise NotImplementedError(
            "This functionality is not implemented for RNN explainers!"
        )

    def get_all_computed_feature_influences(
        self
    ) -> Mapping[ExplainerQiiCacheKey, pd.DataFrame]:
        score_type = self._get_score_type()
        algorithm = ExplanationAlgorithmType.INTEGRATED_GRADIENTS
        cache_dir = self._explanation_cache.get_temp_dir(
            project_name=self._project.name,
            model_name=self._model.name,
            data_collection_name=self._data_collection.name,
            data_split_name=self._base_data_split.name,
            hash_bg=self._attr_config.baseline_split,
            score_type=score_type,
            algorithm=algorithm
        )
        self._load_data_from_cache(cache_dir)
        if self._qiis is None:
            return {}
        return {ExplainerQiiCacheKey(score_type, algorithm): self._qiis}

    def plot_top_k_influence_features(
        self,
        k: int,
        reverse: bool = False,
        qoi_core_class=0,
        qoi_compare_class=None,
        qoi: str = "last",
        qoi_timestep: int = 0,
        from_layer: str = "input",
        pred_thresh: float = 0.5,
        port: int = DASH_PORT
    ):
        """Plot top k features with the highest influence score

        Args:
            k (int): Number of features to show.
            reverse (bool, optional): If set to True, show the top k features with the lowest influence score. Defaults to False.
            qoi_core_class (int, optional): The class that is being explained. default is 0.
            qoi_compare_class (int, optional): A class to compare against. default is None.
            qoi (str, optional): Quantity of interest ["average", "last", "timestep", "first default (ground_truth)", "first default (prediction)"]. Defaults to "average".
            qoi_timestep (int, optional): Used when qoi is set to "timestep": The timestep the influence will be calculated for (reverse indexed where 0 means timestep t-0). Defaults to 0.
            from_layer (str, optional): Layer to calculate the influence from ["input"/"internal"]. Defaults to "input".
            pred_thresh (float, optional): Prediction score threshold. Defaults to 0.5.
            port (int, optional): an open port to run dash server. default is a truera chosen port.
        """
        if qoi not in SUPPORTED_QOI:
            raise ValueError(
                f"Supplied qoi ({qoi}) has to be one of {SUPPORTED_QOI}"
            )
        if qoi_compare_class is None:
            qoi_compare_class = qoi_core_class
        if from_layer not in SUPPORTED_LAYER_NAME:
            raise ValueError(
                f"Supplied from_layer ({from_layer}) has to be one of {SUPPORTED_LAYER_NAME}"
            )
        # Generate data if not already there
        self.get_feature_influences()
        sort = int(reverse)
        viz = self._figures.global_influence_graph(
            top_n=k,
            artifacts_container=self._artifacts_container,
            num_records=len(self._qiis),
            sort=sort,
            qoi=qoi,
            from_layer=from_layer,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh
        )
        # pylint: disable=no-member
        if viz.is_error():
            raise ValueError(
                f"Unable to plot visualization: {viz.get_error_text()}"
            )
        self._show_dash(viz.result, port)

    def _show_dash(self, dash_components, dash_port: int):
        self._app.layout = dash_components
        # Simultaneous Notebooks will have different threads that could block ports. If a port is in use, try the next ones.
        num_retries = 10
        for i in range(num_retries):
            try:
                self._app.run_server(
                    host="0.0.0.0", mode="inline", port=dash_port + i
                )
                break
            except Exception as dash_exc:
                if i < (num_retries - 1):
                    self._logger.info(
                        f"Failed to access dash port, trying port {DASH_PORT + i + 1}. Num retries left: {num_retries - i - 1}"
                    )
                else:
                    raise dash_exc

    def plot_2d_input_influence(
        self,
        feature: str,
        num_timesteps: Optional[int] = None,
        display_timesteps: Optional[int] = None,
        point_index: Union[int, Sequence[int]] = None,
        qoi_core_class: int = 0,
        qoi_compare_class: Optional[int] = None,
        qoi: str = "last",
        qoi_timestep: int = 0,
        pred_thresh: float = 0.5,
        grouping: Optional[str] = None,
        figsize: Tuple[int, int] = (400, 400),
        port: int = DASH_PORT
    ):
        """Plot the 2d influence sensitivity score for a given feature

        Args:
            feature (str): Feature name.
            num_timesteps (int, optional): Only plot the feature influence for that number of input timestep (reverse indexed where 0 means timestep t-0). Defaults to None.
            display_timesteps (int or list[int], optional): show specific timesteps. can be int noting a timestep or a list of timesteps. (reverse indexed where 0 means timestep t-0). Defaults to None.
            point_index (int, optional): Only plot the feature influence for that particular data point. Defaults to None.
            qoi_core_class (int, optional): The class that is being explained. default is 0.
            qoi_compare_class (int, optional): A class to compare against. default is None.
            qoi (str, optional): Quantity of interest ["average", "last", "timestep", "first default (ground_truth)", "first default (prediction)"]. Defaults to "average".
            qoi_timestep (int, optional): Used when qoi is set to "timestep": The timestep the influence will be calculated for (reverse indexed where 0 means timestep t-0). Defaults to 0.
            pred_thresh (float, optional): Prediction score threshold. Defaults to 0.5.
            grouping (str, optional): Color code points according to the grouping. Valid values are ["prediction", "groundtruth", "overfitting", "confusionmatrix"]. Defaults to None.
            figsize (Tuple[int, int], optional): Sizes of the figure (width x height) in pixels. Defaults to (400, 400).
            port (int, optional): an open port to run dash server. default is a truera chosen port.
        """
        self._check_feature_exists(feature)
        if qoi not in SUPPORTED_QOI:
            raise ValueError(
                f"Supplied qoi ({qoi}) has to be one of {SUPPORTED_QOI}"
            )
        # Generate data if not already there
        self.get_feature_influences()
        if qoi_compare_class is None:
            qoi_compare_class = qoi_core_class
        viz = self._figures.feature_temporal_slice_figures(
            feature=feature,
            artifacts_container=self._artifacts_container,
            num_records=len(self._qiis),
            display_timesteps=display_timesteps,
            index=point_index,
            num_timesteps=num_timesteps,
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            grouping=self.STR_TO_GROUPING_OPTION.get(grouping),
            figsize=figsize
        )
        # pylint: disable=no-member
        if viz.is_error():
            raise ValueError(
                f"Unable to plot visualization: {viz.get_error_text()}"
            )
        self._show_dash(viz.result, port)

    def plot_3d_input_influence(
        self,
        feature: str,
        qoi_core_class=0,
        qoi_compare_class=None,
        qoi: str = "last",
        qoi_timestep: int = 0,
        pred_thresh: float = 0.5,
        grouping: Optional[str] = None,
        figsize: Tuple[int, int] = (600, 600)
    ):
        """Plot the 3d influence sensitivity score for a given feature

        Args:
            feature (str): Feature name.
            timestep (int, optional): Only plot the feature influence for that particular input timestep (reverse indexed where 0 means timestep t-0). Defaults to None.
            point_index (int, optional): Only plot the feature influence for that particular data point. Defaults to None.
            qoi_core_class (int, optional): The class that is being explained. default is 0.
            qoi_compare_class (int, optional): A class to compare against. default is None.
            qoi (str, optional): Quantity of interest ["average", "last", "timestep", "first default (ground_truth)", "first default (prediction)"]. Defaults to "average".
            qoi_timestep (int, optional): Used when qoi is set to "timestep": The timestep the influence will be calculated for (reverse indexed where 0 means timestep t-0). Defaults to 0.
            pred_thresh (float, optional): Prediction score threshold. Defaults to 0.5.
            grouping (str, optional): Color code points according to the grouping. Valid values are ["prediction", "groundtruth", "overfitting", "confusionmatrix"]. Defaults to None.
            figsize (Tuple[int, int], optional): Sizes of the figure (width x height) in pixels. Defaults to (800, 300).
        """
        self._check_feature_exists(feature)
        if qoi not in SUPPORTED_QOI:
            raise ValueError(
                f"Supplied qoi ({qoi}) has to be one of {SUPPORTED_QOI}"
            )
        # Generate data if not already there
        self.get_feature_influences()
        if qoi_compare_class is None:
            qoi_compare_class = qoi_core_class
        viz = self._figures.feature_3d_plot(
            feature=feature,
            artifacts_container=self._artifacts_container,
            num_records=len(self._qiis),
            plot_type="scatter",
            qoi_core_class=qoi_core_class,
            qoi_compare_class=qoi_compare_class,
            qoi=qoi,
            qoi_timestep=qoi_timestep,
            pred_thresh=pred_thresh,
            grouping=self.STR_TO_GROUPING_OPTION.get(grouping),
            return_fig=True
        )

        # pylint: disable=no-member
        if viz.is_error():
            raise ValueError(
                f"Unable to plot visualization: {viz.get_error_text()}"
            )
        scatter_fig = viz.result
        scatter_fig.update_layout(
            title_text=feature, width=figsize[0], height=figsize[1]
        )
        scatter_fig.show()

    def get_cache_dir_path(self) -> str:
        return self._explanation_cache.get_temp_dir(
            project_name=self._project.name,
            model_name=self._model.name,
            data_collection_name=self._data_collection.name,
            data_split_name=self._base_data_split.name,
            hash_bg=self._attr_config.baseline_split,
            score_type=self._get_score_type(),
            algorithm=ExplanationAlgorithmType.INTEGRATED_GRADIENTS
        ).name
