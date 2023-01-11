from enum import Enum


class FilterType(Enum):
    AVERAGE_PRED_THRESH = 0
    LAST_STEP_PRED_THRESH = 1
    AVERAGE_LABEL = 2
    LAST_STEP_LABEL = 3
    FEATURE_VAL_CATEGORICAL = 4
    FEATURE_VAL_NUMERIC = 5


class FilterData:

    @staticmethod
    def from_component(filter_component):
        # allow filter_type to be passed in as an attribute for testing
        # otherwise grab filter type from dash component
        filter_type = getattr(filter_component, 'filter_type', None)
        if filter_type is None:
            filter_type = filter_component.component.get_filter_type(
                filter_component.lhs
            )
        return FilterData(
            filter_component.lhs, filter_component.predicate,
            filter_component.rhs, filter_type
        )

    def __init__(self, lhs, predicate, rhs, filter_type=None):
        self.rhs = rhs
        self.lhs = lhs
        self.predicate = predicate
        if isinstance(filter_type, FilterType):
            self.filter_type = filter_type
        else:
            try:
                self.filter_type = FilterType(self.lhs)
            except:
                raise NotImplementedError("Filter type was not provided.")

    def get_filter_type(self, filter_component):
        if isinstance(filter_component.lhs, int):
            return FilterType(filter_component.lhs)

    def is_numeric(self):
        return not 'CATEGORICAL' in self.filter_type.name

    def on_prediction(self):
        return 'PRED' in self.filter_type.name

    def on_label(self):
        return 'LABEL' in self.filter_type.name

    def on_feature_value(self):
        return 'FEATURE_VAL' in self.filter_type.name

    def on_feature_influence(self):
        return 'FEATURE_INF' in self.filter_type.name

    def aggregate_average(self):
        return 'AVERAGE' in self.filter_type.name

    def aggregate_last_step(self):
        return 'LAST_STEP' in self.filter_type.name or not self.is_numeric()
