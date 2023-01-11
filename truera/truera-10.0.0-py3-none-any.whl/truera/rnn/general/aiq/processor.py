import logging

import numpy as np
import pandas as pd
import progressbar

from truera.rnn.general.utils.time import TemporalData

from . import input_inf_utils as ii_utils


# Copied from truera respository, added methods to work with time dimension
class OverfittingProcessor:
    '''
    Class used to process whether overfitting has occurred.
    We can create multiple types of detectors here
    '''
    LOW_DENSITY_THRESHOLD = 0.03
    TOP_PERCENTILE_INFLUENCE = 95

    # Copied from truera respository UNCHANGED
    @classmethod
    def density_diagnostic(cls, infs, data_collection, split_id: str = None):
        data = data_collection.pre_transform_data(split_id).head(len(infs))
        feature_names = data_collection.get_feature_names()
        return OverfittingProcessor.density_diagnostic_low_dens_high_inf(
            infs, data, feature_names
        )

    # Copied from truera respository, modified to add metadata
    @classmethod
    def density_diagnostic_low_dens_high_inf(
        cls, infs, data, feature_names, return_metadata=False
    ):
        '''
        An overfitting diagnostic based on low dense regions. We check to see if
        a top percentile of influence occurs in a low density region of the feature space
        TODO (rick): make it so that LOW_DENSITY_THRESHOLD and TOP_PERCENTILE_INFLUENCE
        are customizable
        '''
        logger = logging.getLogger(__name__ + '.OverfittingProcessor')
        overfit_array = None

        # dict of feature to list of buckets
        bucket_metadata = {}
        # dict of feature to an importance score
        importance_metadata = {}

        for feature in feature_names:

            # Find the TOP_PERCENTILE_INFLUENCE from all the influence data
            # Then for each feature,
            # find whether each point is higher than that threshold
            abs_infs = np.abs(infs)
            abs_inf_vals = np.asarray(abs_infs[feature])
            high_inf = np.percentile(
                abs_infs.values, cls.TOP_PERCENTILE_INFLUENCE
            )
            high_inf_items = abs_inf_vals > high_inf

            feature_vals = data[feature]

            # Find whether points exist in low density regions
            unique, counts = np.unique(feature_vals, return_counts=True)

            is_categorical = len(unique
                                ) < 20 or data.dtypes[feature] == "object"

            if is_categorical:
                density = counts / np.sum(counts)
                # For each category, get its density
                density_dict = dict(zip(unique, density))
                # For each point, convert the category to its density region and check against LOW_DENSITY_THRESHOLD
                low_density_items = np.vectorize(
                    density_dict.__getitem__
                )(feature_vals) < cls.LOW_DENSITY_THRESHOLD

            else:
                hist, bin_edges = np.histogram(
                    feature_vals, bins=20, density=True
                )
                density = hist * np.diff(bin_edges)
                # A little hack so that highest feature value is not part of its own singular bucket
                bin_edges[-1] += 1.0

                # For each point, get its bin
                bin_members = np.digitize(feature_vals, bin_edges)

                # For each point, convert the bin to its density region and check against LOW_DENSITY_THRESHOLD
                low_density_items = np.take(
                    density, bin_members - 1
                ) < cls.LOW_DENSITY_THRESHOLD

            low_density_high_inf = np.logical_and(
                low_density_items, high_inf_items
            )
            if any(low_density_high_inf):
                bucket_metadata[feature] = []
                if is_categorical:
                    bucket_metadata[feature] = [
                        (value, value) for value in
                        np.unique(feature_vals[low_density_high_inf == True])
                    ]

                else:

                    regions = np.unique(
                        bin_members[low_density_high_inf == True]
                    )

                    start = None
                    end = None
                    for i in range(max(bin_members) + 1):
                        if i + 1 in regions:
                            if start is None:
                                start = round(bin_edges[i], 4)
                            end = round(bin_edges[i + 1], 4)
                        else:
                            if start is not None and end is not None:
                                bucket_metadata[feature].append((start, end))
                            start = None
                            end = None

                importance_metadata[feature] = np.percentile(
                    abs_inf_vals[low_density_high_inf == True],
                    cls.TOP_PERCENTILE_INFLUENCE
                )

            low_density_high_inf = np.reshape(
                low_density_high_inf, (len(low_density_high_inf), 1)
            )

            if overfit_array is None:
                overfit_array = low_density_high_inf
            else:
                overfit_array = np.concatenate(
                    (overfit_array, low_density_high_inf), axis=1
                )

        overfit_df = pd.DataFrame(overfit_array, columns=feature_names)
        overfit_df = overfit_df.replace(True, "yes")
        overfit_df = overfit_df.replace(False, "no")
        if return_metadata:
            return overfit_df, bucket_metadata, importance_metadata
        return overfit_df

    @classmethod
    def rnn_density_diagnostic(cls, infs, data, lengths, features, timesteps):
        '''
        transformation method to match input of processor method
        '''
        groups = {}
        data = TemporalData(data, lengths, False).forward_pad_transform()
        infs = TemporalData(infs, lengths, False).forward_pad_transform()
        for feature_idx, feature in enumerate(features):
            diagnostics = []
            for i in range(timesteps):
                data_df = pd.DataFrame(
                    data.get_ndarray()[:, timesteps - i - 1, feature_idx],
                    columns=[feature]
                )
                inf_df = pd.DataFrame(
                    infs.get_ndarray()[:, timesteps - i - 1, feature_idx],
                    columns=[feature]
                )

                # Only use items in valid time sequence for overfitting

                lengths_filter = lengths > i

                data_df = data_df.iloc[lengths_filter]
                inf_df = inf_df.iloc[lengths_filter]

                # set all non valid items to be not overfitting, and overlay the overfit diagnostic DataFrame on top.
                zeros_diagnostic = pd.DataFrame(
                    np.zeros_like(data.get_ndarray()[:, i, feature_idx]),
                    columns=[feature]
                )

                if len(inf_df) > 0:
                    diagnostic = cls.density_diagnostic_low_dens_high_inf(
                        inf_df, data_df, [feature]
                    )
                    diagnostic.index = data_df.index
                    diagnostic = diagnostic.replace("yes", 1)
                    diagnostic = diagnostic.replace("no", 0)
                    zeros_diagnostic.loc[zeros_diagnostic.index.isin(
                        diagnostic.index
                    )] = diagnostic

                diagnostic = zeros_diagnostic
                diagnostics.append(diagnostic.to_numpy())

            overfit_groups = TemporalData(
                np.squeeze(np.moveaxis(np.stack(diagnostics)[::-1], 0, 1)),
                lengths, True
            )
            overfit_groups = overfit_groups.backward_pad_transform()
            groups[feature] = overfit_groups.get_ndarray()

        return groups

    @classmethod
    def rnn_overfit_metadata(cls, infs, data, lengths, features, timesteps):
        '''
        transformation method to match input of processor method
        '''
        data = TemporalData(data, lengths, False).forward_pad_transform()
        infs = TemporalData(infs, lengths, False).forward_pad_transform()

        bucket_metadata = {}
        importance_metadata = {}
        for feature_idx, feature in enumerate(features):
            aggregated_data_df = None
            aggregated_inf_df = None
            for i in range(timesteps):
                data_df = pd.DataFrame(
                    data.get_ndarray()[:, timesteps - i - 1, feature_idx],
                    columns=[feature]
                )
                inf_df = pd.DataFrame(
                    infs.get_ndarray()[:, timesteps - i - 1, feature_idx],
                    columns=[feature]
                )

                # Only use items in valid time sequence for overfitting

                lengths_filter = lengths > i

                data_df = data_df.iloc[lengths_filter]
                inf_df = inf_df.iloc[lengths_filter]
                if aggregated_data_df is None:
                    aggregated_data_df = data_df
                    aggregated_inf_df = inf_df
                else:
                    aggregated_data_df = pd.concat(
                        [aggregated_data_df, data_df], axis=0
                    )
                    aggregated_inf_df = pd.concat(
                        [aggregated_inf_df, inf_df], axis=0
                    )

            _, f_bucket_metadata, f_importance_metadata = cls.density_diagnostic_low_dens_high_inf(
                aggregated_inf_df,
                aggregated_data_df, [feature],
                return_metadata=True
            )
            bucket_metadata = {**bucket_metadata, **f_bucket_metadata}
            importance_metadata = {
                **importance_metadata,
                **f_importance_metadata
            }

        return bucket_metadata, importance_metadata


class SplineProcessor:

    @classmethod
    def var_from_spline_calculation(
        cls,
        all_features,
        total_timesteps,
        influences,
        data,
        lengths,
        length_thresh=None,
        length_thresh_le=False,
        filter_criteria=None,
        poly_order=3
    ):
        diagnostic = {}
        progress = progressbar.ProgressBar(maxval=len(all_features))
        progress.start()
        for f_idx, feature in enumerate(all_features):
            data_3d = ii_utils.data_3d(
                influences[:, :, [f_idx]],
                data[:, :, [f_idx]],
                lengths,
                feature,
                length_thresh=length_thresh,
                length_thresh_le=length_thresh_le,
                sample_filter=filter_criteria
            )
            fitted_data = np.array(
                ii_utils.fit_poly_only(
                    data_3d, total_timesteps, poly_order=poly_order
                )
            )

            for i in range(len(data_3d)):
                points = data_3d[i]
                spline_f = np.poly1d(fitted_data[i])
                vals = np.asarray([point[0] for point in points])
                infs = np.asarray([point[1] for point in points])
                spline_vals = [spline_f(val) for val in vals]

                var_from_spline = np.var(infs - spline_vals)

                if not feature in diagnostic or var_from_spline > diagnostic[
                    feature]:
                    diagnostic[feature] = var_from_spline

            progress.update(progress.currval + 1)
        progress.finish()

        return diagnostic
