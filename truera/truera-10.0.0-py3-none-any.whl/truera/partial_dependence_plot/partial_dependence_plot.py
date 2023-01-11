import logging
from typing import Callable, Mapping, Optional, Sequence, Union
import uuid

import numpy as np
import pandas as pd

from truera.protobuf.public.modelrunner.cache_entries_pb2 import \
    PartialDependenceCache  # pylint: disable=no-name-in-module


class PartialDependencePlotComputer:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def compute_partial_dependence_plot(
        self,
        pre_df: pd.DataFrame,
        post_df: pd.DataFrame,
        transform_if_possible_func: Callable[[pd.DataFrame], pd.DataFrame],
        pre_transform_column_names: Sequence[str],
        post_transform_column_names: Sequence[str],
        feature_map: Mapping[str, Sequence[str]],
        model_func: Callable[[Union[np.ndarray, np.ndarray]],
                             Union[np.ndarray, pd.DataFrame]],
        num_points: int,
        num_samples: int,
        report_progress_func: Callable[[float], None],
        rows: Optional[Sequence[int]] = None
    ) -> PartialDependenceCache:
        post_df = transform_if_possible_func(post_df)
        if rows is not None:
            pre_df = pre_df.iloc[rows]
            post_df = post_df.iloc[rows]
        self.logger.info(f"pre shape = {pre_df.shape}")
        self.logger.info(f"post shape = {post_df.shape}")
        ret = PartialDependenceCache()
        prefeatures = pre_transform_column_names
        ret.prefeatures.extend(prefeatures)
        for idx, prefeature in enumerate(prefeatures):
            xs_pdp, ys_pdp = self.compute_partial_dependence_plot_for_feature(
                model_func, pre_df, post_df, prefeature,
                post_transform_column_names, num_points, num_samples,
                feature_map
            )
            # TODO(davidkurokawa): Instead of using the dtype we should use the one given in the config.
            vals = pre_df[prefeature]
            if pd.api.types.is_integer_dtype(
                vals
            ) or pd.api.types.is_bool_dtype(vals):
                list_to_extend = ret.xs[prefeature].integers
            elif pd.api.types.is_float_dtype(pre_df[prefeature]):
                list_to_extend = ret.xs[prefeature].floats
            elif pd.api.types.is_string_dtype(pre_df[prefeature]):
                list_to_extend = ret.xs[prefeature].strings
            else:
                raise ValueError(
                    f"Column {prefeature} has unexpected dtype: {pre_df.dtypes[prefeature]}!"
                )
            list_to_extend.values.extend(xs_pdp)
            ret.ys[prefeature].values.extend(ys_pdp)
            report_progress_func(100 * (idx + 1) / len(prefeatures))
        return ret

    def compute_partial_dependence_plot_for_feature(
        self,
        model_func: Callable[[Union[pd.DataFrame, np.ndarray]], np.ndarray],
        pre_df: pd.DataFrame,
        post_df: pd.DataFrame,
        prefeature: str,
        postfeatures: Sequence[str],
        num_points: int,
        num_samples: int,
        feature_map: Optional[Mapping[str, Sequence[int]]],
        random_state: int = 0
    ):
        index_col = uuid.uuid4()
        if feature_map:
            postfeatures_of_interest = [
                postfeatures[idx] for idx in feature_map[prefeature]
            ]
        else:
            postfeatures_of_interest = [prefeature]
        feature_vals = post_df[postfeatures_of_interest].copy()
        feature_vals[index_col] = pre_df[prefeature]
        feature_vals.drop_duplicates(inplace=True)
        feature_vals.sort_values(by=index_col, inplace=True)
        num_feature_vals = feature_vals.shape[0]
        if feature_vals.shape[0] >= num_points:
            idxs = np.linspace(0, num_feature_vals - 1, num=num_points)
            idxs = np.floor(idxs)
            idxs = idxs.astype(np.int32)
        else:
            self.logger.info(
                f"Feature `{prefeature}` has {feature_vals.shape[0]} < num_points = {num_points} feature values, so will use all of them."
            )
            idxs = np.array(range(num_feature_vals))
        ret_xs = []
        ret_ys = []
        for idx in idxs:
            if num_samples < post_df.shape[0]:
                xs = post_df.sample(
                    n=num_samples, replace=False, random_state=random_state
                )
            else:
                xs = post_df.copy()
            for postfeature_of_interest in postfeatures_of_interest:
                xs[postfeature_of_interest] = feature_vals[
                    postfeature_of_interest].iloc[idx]
            ys_pred = model_func(xs)
            ret_xs.append(feature_vals[index_col].iloc[idx])
            ret_ys.append(np.mean(ys_pred))
        return ret_xs, ret_ys
