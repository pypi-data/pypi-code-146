import numpy as np

import BasicFeatures
import AggregateFeatures


def compute_all(lat: np.ndarray, lon: np.ndarray, time: np.ndarray, window, threshold,
                window_type=[None, 'time', 'distance']):
    basic_features = []

    basic_features.append(BasicFeatures.speed(lat=lat, lon=lon, time=time))
    basic_features.append(BasicFeatures.acceleration(lat=lat, lon=lon, time=time))
    basic_features.append(BasicFeatures.acceleration2(lat=lat, lon=lon, time=time))
    basic_features.append(BasicFeatures.distance(lat=lat, lon=lon))
    basic_features.append(BasicFeatures.direction(lat=lat, lon=lon))

    if type(threshold) != list:
        threshold = [threshold for _ in basic_features]

    aggregated_features = None
    aggregated_features_time = None
    aggregated_features_distance = None

    index = window_type.index(None) if None in window_type else None
    if index is not None:
        aggregated_features = []
        for features, threshold_value in zip(basic_features, threshold):
            aggregated_features.append(AggregateFeatures.sum(features=features, window=window[index]))
            aggregated_features.append(AggregateFeatures.max(features=features, window=window[index]))
            aggregated_features.append(AggregateFeatures.min(features=features, window=window[index]))
            aggregated_features.append(AggregateFeatures.std(features=features, window=window[index]))
            aggregated_features.append(AggregateFeatures.cov(features=features, window=window[index]))
            aggregated_features.append(AggregateFeatures.var(features=features, window=window[index]))
            aggregated_features.append(AggregateFeatures.rate_upper(features=features, threshold=threshold_value,
                                                                    window=window[index], distance=basic_features[3]))
            aggregated_features.append(AggregateFeatures.rate_below(features=features, threshold=threshold_value,
                                                                    window=window[index], distance=basic_features[3]))
    index = window_type.index('distance') if None in window_type else None
    if index is not None:
        aggregated_features_distance = []
        distance = basic_features[3]
        for features, threshold_value in zip(basic_features, threshold):
            aggregated_features_distance.append(
                AggregateFeatures.sum(features=features, window=window[index], window_type='distance', distance=distance))
            aggregated_features_distance.append(
                AggregateFeatures.max(features=features, window=window[index], window_type='distance', distance=distance))
            aggregated_features_distance.append(
                AggregateFeatures.min(features=features, window=window[index], window_type='distance', distance=distance))
            aggregated_features_distance.append(
                AggregateFeatures.std(features=features, window=window[index], window_type='distance', distance=distance))
            aggregated_features_distance.append(
                AggregateFeatures.cov(features=features, window=window[index], window_type='distance', distance=distance))
            aggregated_features_distance.append(
                AggregateFeatures.var(features=features, window=window[index], window_type='distance', distance=distance))
            aggregated_features_distance.append(
                AggregateFeatures.rate_upper(features=features, threshold=threshold_value,
                                             window=window[index], distance=distance, window_type='distance'))
            aggregated_features_distance.append(
                AggregateFeatures.rate_below(features=features, threshold=threshold_value,
                                             window=window[index], distance=distance, window_type='distance'))

    index = window_type.index('time') if None in window_type else None
    if index is not None:
        aggregated_features_time = []
        for features, threshold_value in zip(basic_features, threshold):
            aggregated_features_time.append(
                AggregateFeatures.sum(features=features, window=window[index], window_type='time', time=time))

            aggregated_features_time.append(
                AggregateFeatures.max(features=features, window=window[index], window_type='time', time=time))

            aggregated_features_time.append(
                AggregateFeatures.min(features=features, window=window[index], window_type='time', time=time))

            aggregated_features_time.append(
                AggregateFeatures.std(features=features, window=window[index], window_type='time', time=time))

            aggregated_features_time.append(
                AggregateFeatures.cov(features=features, window=window[index], window_type='time', time=time))

            aggregated_features_time.append(
                AggregateFeatures.var(features=features, window=window[index], window_type='time', time=time))

            aggregated_features_time.append(
                AggregateFeatures.rate_upper(features=features, threshold=threshold_value, window=window[index],
                                             time=time, window_type='time'))
            aggregated_features_time.append(
                AggregateFeatures.rate_below(features=features, threshold=threshold_value, window=window[index],
                                             time=time, window_type='time'))

    return basic_features, aggregated_features, aggregated_features_time, aggregated_features_distance
