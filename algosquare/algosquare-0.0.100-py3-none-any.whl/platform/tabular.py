"""Processing of tabular data."""
import datetime
import numpy as np
import pandas as pd
import hashlib

from typing import Optional

from ..base.types import Datatype, Metatype, DELIMITER_METATYPES, get_delimiter, is_target_metatype, is_classification_metatype
from ..base.errors import ValidationError

def process_table(data: pd.DataFrame, namespace: Optional[str] = None, metatypes: Optional[dict[Metatype]] = None, include: list[str] = None) -> list[dict]:
    """
    Create metadata for table.

    Args:
        data: DataFrame.
        namespace: string.
        metatypes: dictionary with name and Metatypes.
        include: only compute metadata for specified column names.

    Returns:
        list of dicts.

    Raises:
        ValidationError
    """
    if data.columns.unique().size != data.shape[1]:
        raise ValidationError('columns must be unique')

    output = []
    for name, series in data.items():
        if include is None or name in include:
            datatype, s = _cast_series(series.dropna())

            if datatype == Datatype.VOID:
                metatype = Metatype.VOID
            else:
                if metatypes is None or name not in metatypes:
                    metatype = _infer_metatype(s, name, datatype, namespace)
                else:
                    metatype = metatypes[name]

            metadata = dict(name = name, dtype = datatype, metatype = metatype, feature_id = hashlib.md5(str(name).encode()).hexdigest())

            if metatype != Metatype.VOID:
                _check_metatype(s, name, datatype, metatype, namespace)
                series_stats = _compute_series_stats(s, metatype)
                series_stats['missing'] = data.shape[0] - s.size
                metadata['stats'] = series_stats

            output.append(metadata)

    return output

def _cast_series(s):
    if s.isnull().any():
        raise ValueError('series has null values')

    if not s.size:
        return (Datatype.VOID, None)

    try:
        return (Datatype.INT, s.astype(int))
    except:
        pass

    try:
        return (Datatype.FLOAT, s.astype(float))
    except:
        pass

    return (Datatype.STR, s.astype(str))

def _infer_metatype(s, name, datatype, namespace = None):
    if datatype == Datatype.VOID:
        return Metatype.VOID

    if s.isnull().any():
        raise ValueError('series has null values')

    lowercase = name.lower()
    if lowercase == '' or 'unnamed:' in lowercase:
        return Metatype.VOID

    #void constants
    if not (s != s.iloc[0]).any():
        return Metatype.VOID

    num_unique = s.unique().size
    if datatype == Datatype.INT:
        if num_unique == 2:
            return Metatype.BINARY
        
        if lowercase.endswith('id') and (len(name) == 2 or name[-3] in '_-.:@' or name.endswith('Id')):
            return Metatype.CATEGORICAL

    if namespace == 'targets':
        if datatype in (Datatype.FLOAT, Datatype.INT):
            return Metatype.NUMERICAL
        return Metatype.BINARY if num_unique == 2 else Metatype.CATEGORICAL

    if datatype == Datatype.STR:
        if 'time' in lowercase or 'date' in lowercase:
            return Metatype.DATETIME

        for metatype in DELIMITER_METATYPES:
            delim = get_delimiter(metatype)
            for x in s:
                if delim in x:
                    return metatype

        return Metatype.BINARY if num_unique == 2 else Metatype.CATEGORICAL

    if 'timestamp' in name:
        return Metatype.TIMESTAMP

    return Metatype.NUMERICAL

def _check_metatype(s, name, datatype, metatype, namespace = None):
    if s.isnull().any():
        raise ValueError('series has null values')

    if metatype == Metatype.BINARY:
        if s.unique().size != 2:
            raise ValidationError(f'binary metatype {name} must contain exactly two values')

    if namespace == 'targets':
        if not is_target_metatype(metatype):
            raise ValidationError(f'{name} has invalid target-metatype')
        if datatype == Datatype.FLOAT and metatype != Metatype.NUMERICAL:
            raise ValidationError(f'{name} must be numerical metatype')
        if datatype == Datatype.STR and not is_classification_metatype(metatype):
            raise ValidationError(f'{name} must be binary or categorical metatype')
        if metatype == Metatype.CATEGORICAL:
            if s.unique().size == 2:
                raise ValidationError(f'categorical metatype {name} has two values and should be binary instead')

    try:
        if metatype == Metatype.NUMERICAL:
            s.astype(float)
        elif metatype == Metatype.DATETIME:
            [datetime.datetime.fromisoformat(x) for x in s]
        elif metatype == Metatype.TIMESTAMP:
            [datetime.datetime.fromtimestamp(x) for x in s]
    except:
        raise ValidationError(f'could not convert {name} to {metatype.name.lower()} metatype')

def _compute_series_stats(s, metatype):
    stats = dict()
    #casting ensures stats are json serializable
    if metatype == Metatype.NUMERICAL:
        stats['min'] = float(s.min())
        stats['max'] = float(s.max())
        stats['mean'] = float(s.mean())
        stats['std'] = float(s.std())
        stats['skew'] = float(s.skew())
        stats['kurtosis'] = float(s.kurtosis())
    elif metatype in (Metatype.BINARY, Metatype.CATEGORICAL):
        frequencies = s.value_counts(sort=False)

        if metatype == Metatype.BINARY:
            stats['categories'] = sorted(list(frequencies.index))
        else:
            stats['num_categories'] = int(frequencies.size)
        
        stats['min_count'] = int(frequencies.min())
        stats['max_count'] = int(frequencies.max())
        stats['gini'] = _gini(frequencies)

    return stats

def _gini(counts):
    nominator = 0
    for x in counts:
        for y in counts:
            nominator += np.abs(x-y)
    
    return nominator / (2 * len(counts) * sum(counts))