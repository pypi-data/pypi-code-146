from sonusai.mixture.mixdb import MixtureDatabase
from sonusai.mixture.types import ClassCount
from sonusai.mixture.types import GeneralizedIDs


def get_class_count_from_mixids(mixdb: MixtureDatabase, mixids: GeneralizedIDs = None) -> ClassCount:
    """ Sums the class counts for given mixids
    """
    from sonusai import SonusAIError

    total_class_count = [0] * mixdb.num_classes
    mixids = mixdb.mixids_to_list(mixids)
    for mixid in mixids:
        class_count = mixdb.mixture_class_count(mixid)
        for cl in range(mixdb.num_classes):
            total_class_count[cl] += class_count[cl]

    if mixdb.truth_mutex:
        # Compute the class count for the 'other' class
        if total_class_count[-1] != 0:
            raise SonusAIError('Error: truth_mutex was set, but the class count for the last count was non-zero.')
        total_class_count[-1] = sum([mixdb.mixture_samples(mixid) for mixid in mixids]) - sum(total_class_count)

    return total_class_count
