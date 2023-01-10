from typing import Union

from sonusai.mixture.mixdb import MixtureDatabase
from sonusai.mixture.types import Augmentation


def get_class_balancing_augmentation(mixdb: MixtureDatabase, target_file_index: int) -> Union[Augmentation, None]:
    """ Get the class balancing augmentation rule for the given target
    """
    class_balancing_augmentation = mixdb.class_balancing_augmentation
    if mixdb.targets[target_file_index].class_balancing_augmentation is not None:
        class_balancing_augmentation = mixdb.targets[target_file_index].class_balancing_augmentation
    return class_balancing_augmentation
