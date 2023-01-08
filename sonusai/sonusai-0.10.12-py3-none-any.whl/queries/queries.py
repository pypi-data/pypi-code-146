from typing import Any
from typing import Callable
from typing import Dict
from typing import List

from sonusai.mixture.mixdb import MixtureDatabase
from sonusai.mixture.types import GeneralizedIDs


def get_mixids_from_mixture_field_predicate(mixdb: MixtureDatabase,
                                            field: str,
                                            mixids: GeneralizedIDs = None,
                                            predicate: Callable[[Any], bool] = None) -> Dict[int, List[int]]:
    """
    Generate mixture IDs based on mixture field and predicate
    Return a dictionary where:
        - keys are the matching field values
        - values are lists of the mixids that match the criteria
    """
    from typing import Any

    mixid_out = mixdb.mixids_to_list(mixids)

    if predicate is None:
        def predicate(_: Any) -> bool:
            return True

    criteria = set()
    for i, x in enumerate(mixdb.mixtures):
        if i in mixid_out:
            value = getattr(x, field)
            if isinstance(value, list):
                for v in value:
                    if predicate(v):
                        criteria.add(v)
            elif predicate(value):
                criteria.add(value)
    criteria = sorted(list(criteria))

    result = {}
    for criterion in criteria:
        result[criterion] = []
        for i, x in enumerate(mixdb.mixtures):
            if i in mixid_out:
                value = getattr(x, field)
                if isinstance(value, list):
                    for v in value:
                        if v == criterion:
                            result[criterion].append(i)
                elif value == criterion:
                    result[criterion].append(i)

    return result


def get_mixids_from_truth_settings_field_predicate(mixdb: MixtureDatabase,
                                                   field: str,
                                                   mixids: GeneralizedIDs = None,
                                                   predicate: Callable[[Any], bool] = None) -> Dict[int, List[int]]:
    """
    Generate mixture IDs based on target truth_settings field and predicate
    Return a dictionary where:
        - keys are the matching field values
        - values are lists of the mixids that match the criteria
    """
    from typing import Any

    mixid_out = mixdb.mixids_to_list(mixids)

    # Get all field values
    values = get_all_truth_settings_values_from_field(mixdb, field)

    if predicate is None:
        def predicate(_: Any) -> bool:
            return True

    # Get only values of interest
    values = [value for value in values if predicate(value)]

    result = {}
    for value in values:
        # Get a list of targets for each field value
        indices = []
        for i, target in enumerate(mixdb.targets):
            for truth_setting in target.truth_settings:
                if value in getattr(truth_setting, field):
                    indices.append(i)
        indices = sorted(list(set(indices)))

        mixids = []
        for index in indices:
            mixids.extend([i for i, x in enumerate(mixdb.mixtures) if
                           index in x.target_file_index and i in mixid_out])

        mixids = sorted(list(set(mixids)))
        if mixids:
            result[value] = mixids

    return result


def get_all_truth_settings_values_from_field(mixdb: MixtureDatabase, field: str) -> list:
    """
    Generate a list of all values corresponding to the given field in truth_settings
    """
    result = []
    for target in mixdb.targets:
        for truth_setting in target.truth_settings:
            value = getattr(truth_setting, field)
            if isinstance(value, str):
                value = [value]
            result.extend(value)

    return sorted(list(set(result)))


def get_mixids_from_noise(mixdb: MixtureDatabase,
                          mixids: GeneralizedIDs = None,
                          predicate: Callable[[Any], bool] = None) -> Dict[int, List[int]]:
    """
    Generate mixids based on noise index predicate
    Return a dictionary where:
        - keys are the noise indices
        - values are lists of the mixids that match the noise index
    """
    return get_mixids_from_mixture_field_predicate(mixdb=mixdb,
                                                   mixids=mixids,
                                                   field='noise_file_index',
                                                   predicate=predicate)


def get_mixids_from_noise_augmentation(mixdb: MixtureDatabase,
                                       mixids: GeneralizedIDs = None,
                                       predicate: Callable[[Any], bool] = None) -> Dict[int, List[int]]:
    """
    Generate mixids based on a noise augmentation index predicate
    Return a dictionary where:
        - keys are the noise augmentation indices
        - values are lists of the mixids that match the noise augmentation index
    """
    return get_mixids_from_mixture_field_predicate(mixdb=mixdb,
                                                   mixids=mixids,
                                                   field='noise_augmentation_index',
                                                   predicate=predicate)


def get_mixids_from_target(mixdb: MixtureDatabase,
                           mixids: GeneralizedIDs = None,
                           predicate: Callable[[Any], bool] = None) -> Dict[int, List[int]]:
    """
    Generate mixids based on a target index predicate
    Return a dictionary where:
        - keys are the target indices
        - values are lists of the mixids that match the target index
    """
    return get_mixids_from_mixture_field_predicate(mixdb=mixdb,
                                                   mixids=mixids,
                                                   field='target_file_index',
                                                   predicate=predicate)


def get_mixids_from_target_augmentation(mixdb: MixtureDatabase,
                                        mixids: GeneralizedIDs = None,
                                        predicate: Callable[[Any], bool] = None) -> Dict[int, List[int]]:
    """
    Generate mixids based on a target augmentation index predicate
    Return a dictionary where:
        - keys are the target augmentation indices
        - values are lists of the mixids that match the target augmentation index
    """
    return get_mixids_from_mixture_field_predicate(mixdb=mixdb,
                                                   mixids=mixids,
                                                   field='target_augmentation_index',
                                                   predicate=predicate)


def get_mixids_from_snr(mixdb: MixtureDatabase,
                        mixids: GeneralizedIDs = None,
                        predicate: Callable[[Any], bool] = None) -> Dict[float, List[int]]:
    """
    Generate mixids based on an SNR predicate
    Return a dictionary where:
        - keys are the SNRs
        - values are lists of the mixids that match the SNR
    """
    from typing import Any

    mixid_out = mixdb.mixids_to_list(mixids)

    # Get all the SNRs
    snrs = mixdb.snrs

    if predicate is None:
        def predicate(_: Any) -> bool:
            return True

    # Get only the SNRs of interest (filter on predicate)
    snrs = [snr for snr in snrs if predicate(snr)]

    result = {}
    for snr in snrs:
        # Get a list of mixids for each SNR
        result[snr] = sorted(
            [i for i, x in enumerate(mixdb.mixtures) if x.snr == snr and i in mixid_out and not x.random_snr])

    return result


def get_mixids_from_truth_index(mixdb: MixtureDatabase,
                                mixids: GeneralizedIDs = None,
                                predicate: Callable[[Any], bool] = None) -> Dict[int, List[int]]:
    """
    Generate mixids based on a truth index predicate
    Return a dictionary where:
        - keys are the truth indices
        - values are lists of the mixids that match the truth index
    """
    return get_mixids_from_truth_settings_field_predicate(mixdb=mixdb,
                                                          mixids=mixids,
                                                          field='index',
                                                          predicate=predicate)


def get_mixids_from_truth_function(mixdb: MixtureDatabase,
                                   mixids: GeneralizedIDs = None,
                                   predicate: Callable[[Any], bool] = None) -> Dict[int, List[int]]:
    """
    Generate mixids based on a truth function predicate
    Return a dictionary where:
        - keys are the truth functions
        - values are lists of the mixids that match the truth function
    """
    return get_mixids_from_truth_settings_field_predicate(mixdb=mixdb,
                                                          mixids=mixids,
                                                          field='function',
                                                          predicate=predicate)
