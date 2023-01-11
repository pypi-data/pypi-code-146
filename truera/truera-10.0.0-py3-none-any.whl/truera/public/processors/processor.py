import logging
import math
from typing import Callable, Sequence, Tuple

import numpy as np
import pandas as pd
from sklearn import metrics

from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    FloatTable  # pylint: disable=no-name-in-module


class FitProcessor:

    FITTING_TEMPLATE_PYTHON = '''def {function_name}(x_values):
    import numpy as np
    x_breaks = {x_breaks_list}
    y_breaks = {y_breaks_list}
    return np.interp(x_values, x_breaks, y_breaks)
'''
    # number of precision points to consider as "close" for spline value exclusion. Used as grpc precision can be different from python float precision
    SPLINE_DROP_VAL_MATCH_PRECISION = 4

    @classmethod
    def fit(
        cls,
        x_values,
        y_values,
        x_hint_list,
        y_hint_list,
        function_name="transform"
    ):
        '''
        x_values, y_values originate from the model data.
        x_hint_list, y_hint_list originate from frontend use cases
        '''
        assert len(x_hint_list) == len(y_hint_list)
        assert len(x_values) == len(y_values)
        x_breaks_list = sorted(x_hint_list)
        y_breaks_list = [y for _, y in sorted(zip(x_hint_list, y_hint_list))]
        y_fitted = np.interp(x_values, x_breaks_list, y_breaks_list)
        x_breaks_str = "[{}]".format(','.join(str(x) for x in x_breaks_list))
        y_breaks_str = "[{}]".format(','.join(str(x) for x in y_breaks_list))
        fitting_python_code = FitProcessor.FITTING_TEMPLATE_PYTHON.format(
            function_name=function_name,
            x_breaks_list=x_breaks_str,
            y_breaks_list=y_breaks_str
        )
        logging.getLogger(__name__
                         ).info("Transform code: \n%s", fitting_python_code)
        return metrics.mean_squared_error(
            y_values, y_fitted
        ), fitting_python_code

    @classmethod
    def fit_poly(
        cls,
        x_values: Sequence,
        y_values: Sequence,
        poly_order=3,
        min_x_vals_to_fit=4
    ) -> Tuple[Sequence, Callable]:

        xs = [
            x for i, x in enumerate(x_values)
            if not isinstance(x_values[i], str) and
            not math.isnan(x_values[i]) and not math.isnan(y_values[i])
        ]
        ys = [
            y for i, y in enumerate(y_values)
            if not isinstance(x_values[i], str) and
            not math.isnan(x_values[i]) and not math.isnan(y_values[i])
        ]

        if (len(set(xs)) < min_x_vals_to_fit):
            return None, None
        try:
            fit_coefficients = np.polyfit(xs, ys, poly_order)
            fit_function = np.poly1d(fit_coefficients)
            return fit_coefficients, fit_function
        except:
            logging.getLogger('Processor').info("FitProcessor fit_poly failed")
            return None, None

    @classmethod
    def remove_spline_exclude_vals(
        cls, x: pd.DataFrame, y: pd.DataFrame, spline_exclude_vals: FloatTable
    ):
        x = x.copy(deep=True)
        y = y.copy(deep=True)

        if spline_exclude_vals is None:
            return x, y

        for f in x:
            if spline_exclude_vals.column_value_map[f].values:
                x_vals = x[f].values.tolist()
                drop_x_vals = [
                    round(x, cls.SPLINE_DROP_VAL_MATCH_PRECISION)
                    for x in x_vals
                ]

                exclude_vals = spline_exclude_vals.column_value_map[f].values
                exclude_vals = [
                    round(x, cls.SPLINE_DROP_VAL_MATCH_PRECISION)
                    for x in exclude_vals
                ]
                drop_indices = [
                    i for i, x in enumerate(drop_x_vals) if x in exclude_vals
                ]

                x[f][drop_indices] = np.nan
                y[f][drop_indices] = np.nan
        return x, y

    @classmethod
    def fit_poly_df(
        cls,
        x: pd.DataFrame,
        y: pd.DataFrame,
        poly_order=3,
        resolution=-1,
        include_x_vals=False
    ) -> pd.DataFrame:
        fit_df = pd.DataFrame()
        x_df = pd.DataFrame()
        for f in x:
            x_vals = x[f].values.tolist()
            y_vals = y[f].values.tolist()
            coeff, fit_func = FitProcessor.fit_poly(
                x_vals, y_vals, poly_order=poly_order
            )

            if resolution > 0 and len(x_vals) > 0:
                if not any([isinstance(i, str) for i in x_vals]):
                    min_x = np.nanmin(x_vals)
                    max_x = np.nanmax(x_vals)
                else:
                    min_x = 0
                    max_x = 0
                x_vals = np.linspace(min_x, max_x, resolution).tolist()
            if fit_func is not None:
                fit_df[f] = fit_func(x_vals)
            else:
                fit_df[f] = [np.nan for x in x_vals]

            if include_x_vals:
                x_df[f] = x_vals
        if include_x_vals:
            return x_df, fit_df

        return fit_df


class OverfittingProcessor:
    '''
    Class used to process whether overfitting has occurred. 
    We can create multiple types of detectors here
    '''
    LOW_DENSITY_THRESHOLD = 0.03
    TOP_PERCENTILE_INFLUENCE = 95
    NUM_UNIQUE_FOR_CATEGORICAL = 20
    SPECIAL_VALUE_FUNCTIONS = [
        np.isnan, lambda x: x == np.inf, lambda x: x == -np.inf
    ]

    @classmethod
    def density_diagnostic(
        cls, infs: pd.DataFrame, data: pd.DataFrame
    ) -> pd.DataFrame:
        return OverfittingProcessor.density_diagnostic_low_dens_high_inf(
            infs, data
        )

    @classmethod
    def density_diagnostic_low_dens_high_inf(
        cls, infs: pd.DataFrame, data: pd.DataFrame
    ):
        '''
        An overfitting diagnostic based on low dense regions. We check to see if
        a top percentile of influence occurs in a low density region of the feature space

        TODO (rick): make it so that LOW_DENSITY_THRESHOLD and TOP_PERCENTILE_INFLUENCE
        are customizable
        '''
        overfit_array = None
        abs_infs = np.abs(infs)
        all_infs_flatted = abs_infs.values.flatten()
        high_inf = np.percentile(
            all_infs_flatted[~np.isnan(all_infs_flatted)],
            cls.TOP_PERCENTILE_INFLUENCE
        )
        for feature in data.columns:
            # Find the TOP_PERCENTILE_INFLUENCE from all the influence data
            # Then for each feature,
            # find whether each point is higher than that threshold
            high_inf_items = (abs_infs[feature] > high_inf).to_numpy()
            feature_vals = data[feature]

            # Find whether points exist in low density regions
            if data.dtypes[feature] == "object" or len(
                np.unique(feature_vals)
            ) <= cls.NUM_UNIQUE_FOR_CATEGORICAL:
                value_counts = feature_vals.value_counts(dropna=False)
                value_counts /= value_counts.sum()
                value_counts = value_counts.to_frame().reset_index()
                value_counts.columns = [feature, f"__{feature}_DENSITY__"]
                densities = feature_vals.to_frame().merge(
                    value_counts, on=feature, how='left'
                )[f"__{feature}_DENSITY__"]
                low_density_items = densities.to_numpy(
                ) < cls.LOW_DENSITY_THRESHOLD

            else:
                special_value_masks = [
                    fn(feature_vals) for fn in cls.SPECIAL_VALUE_FUNCTIONS
                ]

                # handle non-special values
                non_special_mask = ~np.logical_or.reduce(special_value_masks)
                num_all = len(non_special_mask)
                num_non_special = np.sum(non_special_mask)
                # TODO(davidkurokawa): This seems like if there's one outlier to the data it will make everything else seem highly dense.
                hist, bin_edges = np.histogram(
                    feature_vals[non_special_mask],
                    bins=cls.NUM_UNIQUE_FOR_CATEGORICAL,
                    density=True
                )
                density = hist * np.diff(bin_edges)
                # A little hack so that highest feature value is not part of its own singular bucket
                bin_edges[-1] += 1.0
                # For each point, get its bin
                bin_members = np.digitize(
                    feature_vals[non_special_mask], bin_edges
                )
                # For each point, convert the bin to its density region and check against LOW_DENSITY_THRESHOLD
                non_special_low_density_items = np.take(
                    density, bin_members - 1
                ) < cls.LOW_DENSITY_THRESHOLD * num_all / num_non_special

                low_density_items = np.zeros(high_inf_items.shape, dtype=bool)
                low_density_items[non_special_mask
                                 ] = non_special_low_density_items

                # handle special values
                for special_value_mask in special_value_masks:
                    special_val_density = np.mean(special_value_mask)
                    low_density_items[
                        special_value_mask
                    ] = special_val_density < cls.LOW_DENSITY_THRESHOLD

            low_density_high_inf = np.logical_and(
                low_density_items, high_inf_items
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

        overfit_df = pd.DataFrame(overfit_array, columns=data.columns)
        overfit_df = overfit_df.replace(True, "yes")
        overfit_df = overfit_df.replace(False, "no")
        return overfit_df
