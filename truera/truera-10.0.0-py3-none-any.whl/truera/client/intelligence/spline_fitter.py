from __future__ import annotations

from typing import Any, Callable, Mapping, Sequence, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from truera.utils.data_utils import is_categorical_feature

_VALID_CONSTRAINTS = [None, "monotonic_inc", "monotonic_dec"]


def _retrieve_from_possible_map(possible_dict, possible_key):
    if isinstance(possible_dict, dict):
        return possible_dict.get(possible_key)
    return possible_dict


class SplineFitter:

    def __init__(
        self, xs: pd.DataFrame, ys: Union[pd.DataFrame, np.ndarray],
        qiis: pd.DataFrame
    ) -> None:
        """Construct a spline fitter.

        Args:
            xs: x-values.
            ys: y-values.
            qiis: QII/influences/shapley-values.
        """
        self._xs = xs
        self._ys = ys
        self._qiis = qiis
        assert sorted(self._xs.columns) == sorted(self._qiis.columns)
        self._valid_features = self._xs.columns
        self._gam = None

    def fit_spline(
        self,
        feature: str,
        n_splines: int = 10,
        spline_order: int = 1,
        constraints: str = None
    ) -> Callable[[Union[pd.Series, np.ndarray]], np.ndarray]:
        """Compute a spline for a single feature.

        Args:
            feature: Feature to compute splines for.
            n_splines: Number of splines per feature. Defaults to 10.
            spline_order: Order of splines. Defaults to 3.
            constraints: The constraints for the spline --- must be one of [None, "monotonic_inc", "monotonic_dec"]. Defaults to None.

        Returns:
            Callable[[Union[pd.Series, np.ndarray]], np.ndarray]: Spline.
        """
        assert feature in self._valid_features, "Invalid feature! Feature {} not in {}.".format(
            feature, self._valid_features
        )
        df = pd.DataFrame.from_dict(
            {
                "xs": self._xs[feature].copy(),
                "ys": self._qiis[feature].copy()
            }
        )
        df.sort_values(by="xs", inplace=True)
        if is_categorical_feature(self._xs[feature]):
            assert constraints is None, "Must have no constraints for categorical features."
            series = df.groupby(["xs"]).mean()["ys"]

            def ret(xs):
                for possible_val in np.unique(xs):
                    if possible_val not in series.index:
                        # If this value has never been seen before, give it a value of 0.
                        series[possible_val] = 0
                if pd.api.types.is_bool_dtype(xs):
                    ret = xs.copy()
                    ret[xs] = series.loc[True]
                    ret[~xs] = series.loc[False]
                else:
                    ret = series.loc[xs].to_numpy()
                return ret

            return ret
        else:
            assert constraints in _VALID_CONSTRAINTS, "Invalid constraint, must be one of {}".format(
                _VALID_CONSTRAINTS
            )
            try:
                import pygam
            except ImportError:
                raise ImportError(
                    "We require pygam, please install via `pip install pygam`."
                )
            spline = pygam.LinearGAM(
                pygam.s(
                    0,
                    n_splines,
                    spline_order=spline_order,
                    constraints=constraints
                )
            )
            spline.fit(df["xs"].values, df["ys"].values)
            return spline.predict

    def construct_gam(
        self,
        n_splines: int = 10,
        spline_orders: int = 3,
        constraints: Union[str, Mapping[str, str]] = None,
        outer_model: Any = LogisticRegression()
    ) -> Pipeline:
        """Construct a GAM based off QII splines.

        Args:
            n_splines: Number of splines per feature. Defaults to 10.
            spline_orders: Order of splines. Defaults to 3.
            constraints: If a single str, then the constraints for all features. Otherwise a dict from feature to constraints. All constraints must be one of [None, "monotonic_inc", "monotonic_dec"]. Defaults to None.
            outer_model: Model to combine splines. This must work with sklearn.pipeline.Pipeline. Defaults to LogisticRegression().

        Returns:
            Pipeline: GAM model.
        """
        all_feature_spline_transform = AllFeatureSplineTransform(
            self, self._valid_features, n_splines, spline_orders, constraints
        )
        pipeline = Pipeline(
            [
                ("all_feature_spline_transform", all_feature_spline_transform),
                ("outer_model", outer_model),
            ]
        )
        pipeline.fit(self._xs, self._ys)
        self._gam = pipeline
        return pipeline

    def plot_isp(
        self, feature: str, figsize: Tuple[int, int] = (21, 6)
    ) -> None:
        """Plot the influence sensitivity plot (ISP) of a specific feature along with the associated spline.

        Args:
            feature: Feature to plot the ISP of.
            figsize: Size for plot. Defaults to (21, 6).
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError(
                "We require matplotlib. Consider installing via `pip install matplotlib`."
            )
        assert self._gam is not None, "Must call construct_gam first!"
        assert feature in self._valid_features
        feature_values = self._xs[feature]
        is_categorical = is_categorical_feature(feature_values)
        if is_categorical:
            xs = np.unique(feature_values)
            xs = np.sort(xs)
        else:
            xs = np.linspace(
                np.min(feature_values), np.max(feature_values), num=1000
            )
        spline_values = self._gam.named_steps["all_feature_spline_transform"
                                             ].get_spline(feature)(xs)
        #spline_values = splines[feature](xs)
        plt.figure(figsize=figsize)
        plt.title(feature)
        plt.xlabel("feature values")
        plt.ylabel("QIIs & spline")
        plt.scatter(feature_values, self._qiis[feature], c="blue", s=1)
        if is_categorical:
            plt.scatter(xs, spline_values, c="red", s=20)
        else:
            plt.plot(xs, spline_values, c="red")
        plt.show()

    def plot_isps(
        self,
        features: Sequence[str] = None,
        figsize: Tuple[int, int] = (21, 6)
    ) -> None:
        """Plot the influence sensitivity plot (ISP) of a set of features along with the associated spline.

        Args:
            features: Features to plot the ISP of. Defaults to None, which is all features.
            figsize: Size for plot. Defaults to (21, 6).
        """
        features = features or self._valid_features
        for feature in features:
            self.plot_isp(feature, figsize=figsize)


class AllFeatureSplineTransform:

    def __init__(
        self, spline_fitter: SplineFitter, valid_features: Sequence[str],
        n_splines: int, spline_orders: int,
        constraints: Union[str, Mapping[str, str]]
    ) -> None:
        self._spline_fitter = spline_fitter
        self._valid_features = valid_features
        self._n_splines = n_splines
        self._spline_orders = spline_orders
        self._constraints = constraints

    def fit(self, xs, ys) -> AllFeatureSplineTransform:
        self._splines = {}
        for feature in self._valid_features:
            n_splines = _retrieve_from_possible_map(self._n_splines, feature)
            spline_order = _retrieve_from_possible_map(
                self._spline_orders, feature
            )
            constraints = _retrieve_from_possible_map(
                self._constraints, feature
            )
            self._splines[feature] = self._spline_fitter.fit_spline(
                feature,
                n_splines=n_splines,
                spline_order=spline_order,
                constraints=constraints
            )
        return self

    def transform(self, xs: pd.DataFrame) -> pd.DataFrame:
        transformed_mp = {}
        for feature in self._valid_features:
            transformed_mp[feature] = self._splines[feature](xs[feature])
        return pd.DataFrame.from_dict(transformed_mp)

    def get_spline(
        self, feature: str
    ) -> Callable[[Union[pd.Series, np.ndarray]], np.ndarray]:
        return self._splines[feature]
