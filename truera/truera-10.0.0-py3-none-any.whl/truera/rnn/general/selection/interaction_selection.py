from enum import Enum
from enum import unique

from dash import dcc
import numpy as np


class DropdownEnum(Enum):

    @classmethod
    def option_to_label(cls):
        raise NotImplementedError


@unique
class FeatureSpace(DropdownEnum):
    INPUT = 0
    ATTRIBUTION = 1

    @classmethod
    def option_to_label(cls):
        return {cls.INPUT: 'Input Space', cls.ATTRIBUTION: 'Influence Space'}


@unique
class AggregationMethod(DropdownEnum):
    MEAN = 'mean'
    MAX = 'max'
    VAR = 'var'
    L1 = 1
    L2 = 2

    @classmethod
    def option_to_label(cls):
        return {
            cls.MEAN: 'Average',
            cls.MAX: 'Maximum',
            cls.VAR: 'Variance',
            cls.L1: 'L1 Norm',
            cls.L2: 'L2 Norm'
        }


@unique
class InteractionType(DropdownEnum):
    CORRELATION = 0
    PARTIAL_CORRELATION = 1
    AUTO_CORRELATION = 2

    @classmethod
    def option_to_label(cls):
        return {
            cls.CORRELATION: 'Correlation',
            cls.PARTIAL_CORRELATION: 'Partial Correlation',
            cls.AUTO_CORRELATION: 'Autocorrelation',
        }


@unique
class InteractAlong(DropdownEnum):
    FEATURE_DIM = 0
    TEMPORAL_DIM = 1
    ALL = 2

    @classmethod
    def option_to_label(cls):
        return {
            cls.FEATURE_DIM: 'Feature-wise Interaction',
            cls.TEMPORAL_DIM: 'Temporal Interaction',
            cls.ALL: 'All Features',
        }


@unique
class FeatureInteractionPage(DropdownEnum):
    INTERNAL_ATTR = 0
    PAIRWISE = 1

    @classmethod
    def option_to_label(cls):
        return {
            cls.INTERNAL_ATTR: 'Internal Attributions',
            cls.PAIRWISE: 'Pairwise Feature Interactions',
        }


@unique
class SortingMode(DropdownEnum):
    MANUAL = 0
    VAR_ASCENDING = 1
    VAR_DESCENDING = 2

    @classmethod
    def option_to_label(cls):
        return {
            cls.MANUAL: 'Manual',
            cls.VAR_ASCENDING: 'Ascending',
            cls.VAR_DESCENDING: 'Descending',
        }


@unique
class LocalExpSortMode(DropdownEnum):
    DESCENDING = 'DESCENDING'
    ASCENDING = 'ASCENDING'
    NONE = 'NONE'

    @classmethod
    def option_to_label(cls):
        return {
            cls.DESCENDING: 'Most Positive Influence',
            cls.ASCENDING: 'Most Negative Influence',
            cls.NONE: 'None'
        }

    @classmethod
    def get_sort_order(cls, sort_mode, df, col_name):
        if sort_mode == 'ASCENDING':
            return df.sort_values(by=col_name, ascending=True)
        elif sort_mode == 'DESCENDING':
            return df.sort_values(by=col_name, ascending=False)
        else:
            return df


@unique
class ModelGrouping(DropdownEnum):
    NONE = 'NONE'
    OVERFITTING = 'OVERFITTING'
    PREDICTION = 'PREDICTION'
    GROUND_TRUTH = 'GROUND_TRUTH'
    CONFUSION_MATRIX = 'CONFUSION_MATRIX'

    @classmethod
    def option_to_label(cls):
        return {
            cls.NONE: 'None',
            cls.OVERFITTING: 'Overfitting',
            cls.PREDICTION: 'Prediction',
            cls.GROUND_TRUTH: 'Ground truth',
            cls.CONFUSION_MATRIX: 'Confusion matrix'
        }


@unique
class InfluenceAggregationMethod(DropdownEnum):
    MEAN_ABS = 'mean'
    VAR = 'var'
    MAX_VALUE = 'max'
    MIN_VALUE = 'min'

    def apply_aggregation(self, arr, axis=None):
        if self.name == 'MEAN_ABS':
            return np.mean(np.abs(arr), axis=axis)
        else:
            fn = getattr(np, self.value)
            return fn(arr, axis=axis)

    @classmethod
    def option_to_label(cls):
        return {
            cls.MEAN_ABS: 'Mean Absolute Value',
            cls.VAR: 'Variance',
            cls.MAX_VALUE: 'Maximum Value',
            cls.MIN_VALUE: 'Minimum Value'
        }


@unique
class GroupProfilerDiagnosticType(Enum):
    INFLUENCE_CONCENTRATION = 'Influence Concentration'
    NO_STRONG_INFLUENCE = 'No Strong Influence'


@unique
class GlobalExplanationView(Enum):
    INFLUENCE_DISTRIBUTION = 'Influence Distribution'
    VALUE_DISTRIBUTION = 'Feature Value Distribution'
    INFLUENCE_SENSITIVITY_PLOTS = 'Influence Sensitivity Plots'


@unique
class FeaturePageView(Enum):
    OVERVIEW_HEATMAP = 'Overview Heatmap'
    TEMPORAL_SLICE = 'Temporal Slice'
    TEMPORAL_TRENDS = 'Temporal Trends'
    THREE_D_PLOT = '3-D Plot'


def get_dropdown_from_enum(id, dropdown_enum, default_enum):
    options_to_labels = dropdown_enum.option_to_label()
    model_dropdown = dcc.Dropdown(
        id=id,
        options=[
            {
                'label': label,
                'value': option.value
            } for option, label in options_to_labels.items()
        ],
        placeholder=options_to_labels[default_enum],
        value=default_enum.value
    )
    return model_dropdown
