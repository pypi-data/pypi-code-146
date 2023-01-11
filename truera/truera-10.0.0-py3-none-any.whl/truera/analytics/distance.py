"""
# Distance metrics: given two sets of samples (typically of the same feature from different splits), produce
# a number representing distance between the two sets of samples. Some may not be strictly metrics/distances
# in the mathematical sense.

## Basic usage:

   Metrics for categorical features:
        for metric_enum, metric in MetricComputers.Categorical.all.items():
             metric_value = metric.distance_of_samples(series1, series2)

   Metrics for numerical features:
        for metric_enum, metric in MetricComputers.Numerical.all.items():
             metric_value = metric.distance_of_samples(series1, series2)

   Above metric_enum is the metric's protobuf enum index and metric_value is the distance value.

## Further details:

Metrics are organized in a class hierarchy all deriving from Distance which publicly exposes one method:

   distance_of_samples(series1: T_Samples, series2: T_Samples) -> Double

This takes two pandas series of values of some feature and returns the distance metric result as a double.
The collection of current metrics is organized into MetricComputers class containing Categorical and Numerical with
each having some metrics of their respective types. To work with numerical Wasserstein, for example:

   metric: Distance = MetricComputers.Numerical.Wasserstein()
   dist: np.double = metric.distance_of_samples(series1, series2)

Constructing instances of metric classes is not necessary as all of their contents are class fields
and class methods but if you want to use the hierarchy, it may be useful. For example, you can check whether
a metric is for categorical fields using:

   if isinstance(metric, CategoricalDistance): ...

Because all categorical metrics derive from CategoricalDistance which in turn derives from
Distance. Interacting with protobuf is not difficult as each metric class contain a reference to the
enum index that represents it:

  metric.type_proto

Also, given a enum index and type (numerical/categorical), you can look up an instance of that metric class:

  MetricComputers.Categorical.all[metric.type_proto]

"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections import defaultdict
from typing import Callable, Iterable, Mapping, Set, Tuple, TypeVar

import numpy as np
from pandas import Series
import pandas as pd
from pandas.api import types as pd_types
import scipy
import scipy.stats as stats
import sklearn.neighbors

from truera.protobuf.public.aiq import distance_pb2 as proto

# proto enum of the types of distance metrics
types_proto = proto.DistanceType

# Type for feature value, or "elements".
T_Value = TypeVar("T_Value")

# Type for domains (of samples): a set (hence unique) of elements.
T_Domain = Set[T_Value]

# Class/Type for probability values.
Prob = np.double

# Class/Type for distance results.
DistanceValue = np.double

# Class/Type for samples: pandas series.
Samples = Series

# Type for distributions: sample value to probability maps.
T_Distribution = Mapping[T_Value, Prob]

# Type for linearized distributions. Elements are indices in the array and their probabilities are the
# values.
T_LinearDistribution = np.ndarray  # elements are Prob

# Type for implementations of distance that take in samples. Numerical distance metrics
# are implemented this way.
T_FuncDistanceOfSamples = Callable[[Samples, Samples], DistanceValue]

# Type for implementations of distance that take linearized distributions. Categorical
# distance metrics are implemented this way so samples may need to be first converted
# to linear distributions.
T_FunDistanceOfLinearDistributions = Callable[
    [T_LinearDistribution, T_LinearDistribution], DistanceValue]

# Small double for numerical stability of metrics with division by zero (prob) issues.
EPSILON = Prob(0.000001)

# For slow operations, sample down to this many samples.
MAX_SAMPLES = 50000


# NOTE(piotrm) pandas method below considers bools numerical but this would give us problems later on. Better to
# mostly view them as categorical.
def dtype_is_numerical(dtype: np.dtype):
    if bool == dtype:
        return False

    return pd_types.is_numeric_dtype(dtype)


# NOTE(piotrm) the pandas method below seems to work except they consider objects not
# categorical while most of our non-explicitly typed fields and up having dtype object.
def dtype_is_categorical(dtype: np.dtype):
    if object == dtype:
        return True

    if bool == dtype:
        return True

    return pd_types.is_categorical_dtype(dtype)


def _common_domain(*dists: Iterable[T_Distribution]) -> T_Domain:
    """Given a set of distributions, find the domain they share."""

    domain = set()

    for dist in dists:
        dist: T_Distribution
        domain = domain.union(set(dist.keys()))

    return domain


def _linearize_distribution(
    dist: T_Distribution, domain: T_Domain
) -> T_LinearDistribution:
    """Convert the given distribution into a linear one one the given domain."""

    return np.array([dist[idx] + EPSILON for idx in domain])


def _linearize_on_common_domain(*dists: Iterable[T_Distribution]):
    # -> (T_Domain, Iterable[T_LinearDist]):
    # The return type hint above is not quite right but unsure how to make it right.
    """Convert the given set of distributions into linear ones one their common domain. Also
    return that domain.
    """
    domain = sorted(_common_domain(*dists))

    return (domain, *[_linearize_distribution(dist, domain) for dist in dists])


# TODO(piotrm): similar implemented anywhere?
def _distribution_of_samples(series: Samples) -> T_Distribution:
    """Convert a set of samples into its empirical distribution."""

    counts = defaultdict(int)
    for element in series:
        counts[element] += 1

    total = len(series)

    return defaultdict(
        float, {
            element: Prob(count) / Prob(total)
            for element, count in counts.items()
        }
    )


def _imp_samples_of_imp_linear_distributions(
    imp: T_FunDistanceOfLinearDistributions
) -> T_FuncDistanceOfSamples:
    """Given a metric implementation that operates on linear distributions, create
    the equivalent that operates on samples instead."""

    def imp_of_series(series1: Series, series2: Series):
        _, l_dist1, l_dist2 = _linearize_on_common_domain(series1, series2)
        return imp(l_dist1, l_dist2)

    return imp_of_series


def _linear_distributions_of_samples(
    series1: Samples, series2: Samples
) -> (T_LinearDistribution, T_LinearDistribution):
    """Convert two series of samples to linear distributions over their common
    domain."""

    dist1 = _distribution_of_samples(series1)
    dist2 = _distribution_of_samples(series2)

    domain, l_dist1, l_dist2 = _linearize_on_common_domain(dist1, dist2)

    return l_dist1, l_dist2


def _bucket_numerical_samples_by_quantiles(
    series1: Samples, series2: Samples, num_bins: int
) -> Tuple[Samples, Samples]:
    """Create categorical samples of the given numerical series by binning values into num_bins of approximtely the
    same cardinality according to the first series. Thus the bins become first-series quantiles.
    """

    quants = np.quantile(series1, np.linspace(0.0, 1.0, num_bins + 1))
    quants[0] = -np.inf
    quants[num_bins] = np.inf

    dist1 = np.digitize(series1, quants)
    dist2 = np.digitize(series2, quants)

    return Samples(dist1), Samples(dist2)


def _pmf_of_numerical_samples(
    series: Samples, min_val: float, max_val: float, num_bins: int
):
    """Convert a set of numerical samples into pmf where the bins are equally spaced"""
    domain = np.linspace(min_val, max_val, num_bins)

    if len(series) > MAX_SAMPLES:
        series = series.sample(MAX_SAMPLES)

    if len(series.shape) < 2:
        series = np.expand_dims(series, axis=1)

    kde_bandwidth = _estimate_bandwidth_for_kde(series)
    kde = sklearn.neighbors.KernelDensity(bandwidth=kde_bandwidth).fit(series)
    domain_score = np.exp(kde.score_samples(np.expand_dims(domain, axis=1)))
    return domain, domain_score / np.sum(domain_score)


def _estimate_bandwidth_for_kde(series: Samples):
    """Estimate appropriate bandwidth for KDE given a set of numerical samples
    Approach implemented here is called the 'rule of thumb' approach where there is some
    assumption that the underlying data is somewhat Gaussian (or mixture of some low number
    of Gaussians). The risk of applying this to data that is very far from Gaussian is
    things may be oversmoothed, but that's OK given our use case of this."""
    if series.dtype == bool:
        series = series.astype(np.int64)
    bw = 0.9 * min(np.std(series),
                   stats.iqr(series) / 1.34) * np.power(len(series), -1 / 5)
    if bw < 1e-3:
        bw = 0.9 * np.std(series) * np.power(len(series), -1 / 5)
    return max(bw, 1e-5)


class Distance(ABC):
    """
    A distance metric computes "distance" between a feature in two sources where each source
    is either a set of samples or a linear probability distribution.
    """

    # TODO(piotrm): want to make this an abstract attribute but there doesn't
    # seem to be any good options for doing this in python 3.7 .
    name: str = None

    # The instance of types_proto that corresponds to this metric if available.
    type_proto = None

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

    # Distance is computed from one of two possible data sources, Samples or
    # "linear" distributions (see documentation on their types above). Raw data is in the form
    # of samples so they may need to be converted.
    #
    # Categorical distance metrics do this conversion to use various scipy implementations which
    # require linear distributions. Numeric distance metrics operate on samples directly and
    # are not converted; the scipy implementations operate on samples.

    @classmethod
    @abstractmethod
    def distance_of_linear_distributions(
        cls, l_dist1: T_LinearDistribution, l_dist2: T_LinearDistribution
    ) -> DistanceValue:
        """Compute the distance result based on two linear distributions. Made private
        for now."""
        pass

    @classmethod
    @abstractmethod
    def distance_of_samples(
        cls, series1: Samples, series2: Samples
    ) -> DistanceValue:
        """Compute the distance result based on two sets of samples."""
        pass

    @classmethod
    def distance_of_samples_iterable(
        cls, samples1: Iterable[T_Value], samples2: Iterable[T_Value]
    ) -> DistanceValue:
        """Get the distance given two iterables of samples."""

        return cls.distance_of_samples(Series(samples1), Series(samples2))


class NumericalDistance(Distance, ABC):
    """Class of numerical distance metrics. Shared types are included in this class but implementations
    of distance are left are abstract for subclasses to implement."""

    @classmethod
    def distance_of_linear_distributions(
        cls, l_dist1: T_LinearDistribution, l_dist2: T_LinearDistribution
    ) -> DistanceValue:
        # Putting this method here so subclasses do not have to implement it
        # over and over.
        raise NotImplementedError(
            "numeric distances do not support distribution inputs"
        )


class CategoricalDistance(Distance, ABC):
    """Class of categorical distance metrics."""

    @classmethod
    def distance_of_samples(
        cls, series1: Samples, series2: Samples
    ) -> DistanceValue:
        l_dist1, l_dist2 = _linear_distributions_of_samples(series1, series2)
        return cls.distance_of_linear_distributions(l_dist1, l_dist2)


class LNormDistance(CategoricalDistance, ABC):
    """Parent of the norm-based metrics. Here to be able to use types for sorting through them."""
    pass


def _create_lnorm_metric(ord: float = 1):
    """Create an L* norm-based metric for any given *. """

    class LAny(LNormDistance):
        ord = ord
        name: str = f"L{ord}"

        @classmethod
        def distance_of_linear_distributions(
            cls, l_dist1: T_LinearDistribution, l_dist2: T_LinearDistribution
        ) -> DistanceValue:
            return DistanceValue(np.linalg.norm(l_dist1 - l_dist2, ord=ord))

    # Rename the class to its name string as otherwise all norm metrics will be named the same "LAny".
    LAny.__name__ = LAny.name
    return LAny


class DistanceComputers(object):
    """Container class with implementations of the various metrics."""

    class Numerical(object):
        """Container for numerical metrics."""

        class Wasserstein(NumericalDistance):
            """Wasserstein metric, aka earthmover distance. Scale is as underlying domain."""
            name: str = "Wasserstein"
            type_proto = types_proto.NUMERICAL_WASSERSTEIN

            @classmethod
            def distance_of_samples(
                cls, series1: Samples, series2: Samples
            ) -> DistanceValue:
                return DistanceValue(
                    stats.wasserstein_distance(series1, series2)
                )

        class DifferenceOfMean(NumericalDistance):
            """Difference of means. Scale is as underlying domain."""
            name: str = "Difference of Mean"
            type_proto = types_proto.DIFFERENCE_OF_MEAN

            @classmethod
            def distance_of_samples(
                cls, series1: Samples, series2: Samples
            ) -> DistanceValue:
                # NOTE(piotrm): not a distance metric as it is signed, can be negative. Need to
                # better organize or distinguish signed values from metrics eventually.
                return DistanceValue(series2.mean() - series1.mean())

        class JensenShannonDistance(NumericalDistance):
            """Numeric version of JS Distance. This metric makes some statistic assumptions and approximations."""
            name: str = "Jensen-Shannon Distance"
            type_proto = types_proto.NUMERICAL_JENSEN_SHANNON_DISTANCE

            @classmethod
            def distance_of_samples(
                cls, series1: Samples, series2: Samples
            ) -> DistanceValue:

                series_concat = pd.concat([series1, series2], ignore_index=True)
                min_val = np.min(series_concat)
                max_val = np.max(series_concat)
                num_bins = min(len(np.unique(series_concat)), 100)
                _, pmf1 = _pmf_of_numerical_samples(
                    series1, min_val, max_val, num_bins
                )
                _, pmf2 = _pmf_of_numerical_samples(
                    series2, min_val, max_val, num_bins
                )

                return DistanceValue(
                    scipy.spatial.distance.jensenshannon(pmf1, pmf2, base=2)
                )

        class EnergyDistance(NumericalDistance):
            name: str = "Energy Distance"
            type_proto = types_proto.ENERGY_DISTANCE

            @classmethod
            def distance_of_samples(
                cls, series1: Samples, series2: Samples
            ) -> DistanceValue:
                return DistanceValue(
                    scipy.stats.energy_distance(series1, series2)
                )

        class KolmogorovSmirnovStatistic(NumericalDistance):
            """Kolmogorov-Smirnov statistic. The implementation produces also a confidence p-value but we are
            currently not using it."""
            name: str = "Kolmogorov-Smirnov Statistic"
            type_proto = types_proto.KOLMOGOROV_SMIRNOV_STATISTIC

            @classmethod
            def distance_of_samples(
                cls, series1: Samples, series2: Samples
            ) -> DistanceValue:
                return DistanceValue(
                    scipy.stats.kstest(rvs=series1, cdf=series2)[0]
                )

        class PopulationStabilityIndex(NumericalDistance):
            name: str = "(Baseline-Deciled) Population Stability Index"
            type_proto = types_proto.NUMERICAL_POPULATION_STABILITY_INDEX

            @classmethod
            def distance_of_samples(
                cls, series1: Samples, series2: Samples
            ) -> DistanceValue:

                # Convert into categorical samples by binning into 10 bins of equal series1 frequency.
                # TODO(piotrm): Description of PSI on https://www.listendata.com/2015/05/population-stability-index.html
                # suggests that the bins or "deciles" are provided externally by expert instead of being
                # equal-frequency series1 bins. We do not currently have this data so leaving it as a TODO item for
                # the future.
                # NOTE(piotrm): Alternatively we could use segments to specify this but that would require a lot
                # of work.
                series1_, series2_ = _bucket_numerical_samples_by_quantiles(
                    series1, series2, 10
                )

                return DistanceComputers.Categorical.PopulationStabilityIndex.distance_of_samples(
                    series1_, series2_
                )

        # All numeric metrics for easier processing.
        all: Mapping[types_proto, NumericalDistance] = {
            cls.type_proto: cls for cls in [
                Wasserstein(),
                DifferenceOfMean(),
                JensenShannonDistance(),
                EnergyDistance(),
                KolmogorovSmirnovStatistic(),
                PopulationStabilityIndex()
            ]
        }

    class Categorical(object):
        """Container for all categorical metrics."""

        class WassersteinOrdered(CategoricalDistance):
            """Ordered Wasserstein, aka ordered earthmover distance. This orders values
            on the scale of 0 to |domain|-1 and uses positions on this scale to determine
            distance. The position is determined by sorting so at least it is deterministic."""

            name: str = "Ordered Wasserstein"
            type_proto = types_proto.CATEGORICAL_WASSERSTEIN_ORDERED

            @classmethod
            def distance_of_linear_distributions(
                cls, l_dist1: T_LinearDistribution,
                l_dist2: T_LinearDistribution
            ) -> DistanceValue:
                domain = np.arange(0, len(l_dist1))

                # To compute ordered wasserstein, we use the weights parameters to the stats
                # method and pass in the distributions there. The samples are set to the whole
                # domain.
                return DistanceValue(
                    stats.wasserstein_distance(
                        domain, domain, l_dist1, l_dist2
                    )
                )

        class WassersteinUnordered(CategoricalDistance):
            """Unordered Wasserstein, aka unordered earthmover distance, aka total variation distance, aka 1/2
            of L1 distance. """

            name: str = "Unordered Wasserstein"
            type_proto = types_proto.CATEGORICAL_WASSERSTEIN_UNORDERED

            @classmethod
            def distance_of_linear_distributions(
                cls, l_dist1: T_LinearDistribution,
                l_dist2: T_LinearDistribution
            ) -> DistanceValue:
                # This metric is equivalent to total variation distance.
                return DistanceComputers.Categorical.TotalVariation.distance_of_linear_distributions(
                    l_dist1, l_dist2
                )

        class TotalVariation(CategoricalDistance):
            """Total variation distance, aka 1/2 of L1 distance. """

            name: str = "Total Variation Distance"
            type_proto = types_proto.TOTAL_VARIATION_DISTANCE

            @classmethod
            def distance_of_linear_distributions(
                cls, l_dist1: T_LinearDistribution,
                l_dist2: T_LinearDistribution
            ) -> DistanceValue:
                # This metric is equivalent to 1/2 of l1 distance.
                return DistanceValue(
                    0.5 * DistanceComputers.Categorical.L1Distance.
                    distance_of_linear_distributions(l_dist1, l_dist2)
                )

        class JensenShannonDistance(CategoricalDistance):
            name: str = "Jensen-Shannon Distance"
            type_proto = types_proto.CATEGORICAL_JENSEN_SHANNON_DISTANCE

            @classmethod
            def distance_of_linear_distributions(
                cls, l_dist1: T_LinearDistribution,
                l_dist2: T_LinearDistribution
            ) -> DistanceValue:

                return DistanceValue(
                    scipy.spatial.distance.jensenshannon(
                        l_dist1, l_dist2, base=2
                    )
                )

        class ChiSquareTest(CategoricalDistance):
            """Chi-Square Test. This one comes with a p-value which are currently not using."""

            name: str = "Chi-Square Test"
            type_proto = types_proto.CHI_SQUARE_TEST

            @classmethod
            def distance_of_linear_distributions(
                cls, l_dist1: T_LinearDistribution,
                l_dist2: T_LinearDistribution
            ) -> DistanceValue:

                return DistanceValue(scipy.stats.chisquare(l_dist1, l_dist2)[0])

        class PopulationStabilityIndex(CategoricalDistance):
            name: str = "Population Stability Index"
            type_proto = types_proto.CATEGORICAL_POPULATION_STABILITY_INDEX

            @classmethod
            def distance_of_linear_distributions(
                cls, l_dist1: T_LinearDistribution,
                l_dist2: T_LinearDistribution
            ) -> DistanceValue:

                # NOTE(piotrm): Description on https://www.listendata.com/2015/05/population-stability-index.html
                # suggests natural log should be used though log-2 would be more consistent with the information
                # theoretic distances. Keeping it as natural for now (np.log is natural log).
                return DistanceValue(
                    np.sum((l_dist2 - l_dist1) * np.log(l_dist2 / l_dist1))
                )

        class L1Distance(_create_lnorm_metric(ord=1)):
            """L1 distance, aka unordered wasserstein. aka 2 * total variation. """
            type_proto = types_proto.L1

        class L2Distance(_create_lnorm_metric(ord=2)):
            """L2 distance, aka euclidean distance."""
            type_proto = types_proto.L2

        class LInfDistance(_create_lnorm_metric(ord=np.inf)):
            """L-Infinity distance."""
            type_proto = types_proto.LInfinity

        # All categorical metrics can be accessed though this map.
        all: Mapping[types_proto, CategoricalDistance] = {
            cls.type_proto: cls for cls in [
                WassersteinUnordered(),
                WassersteinOrdered(),
                TotalVariation(),
                JensenShannonDistance(),
                ChiSquareTest(),
                PopulationStabilityIndex(),
                L1Distance(),
                L2Distance(),
                LInfDistance()
            ]
        }
