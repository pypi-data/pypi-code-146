from typing import List

from sonusai.mixture.mixdb import MixtureDatabase
from sonusai.mixture.types import Augmentations
from sonusai.mixture.types import AugmentedTarget
from sonusai.mixture.types import AugmentedTargets
from sonusai.mixture.types import TargetFile
from sonusai.mixture.types import TargetFiles


def get_augmented_targets(target_files: TargetFiles, target_augmentations: Augmentations) -> AugmentedTargets:
    from sonusai.mixture import get_augmentation_indices_for_mixup
    from sonusai.mixture import get_mixups

    mixups = get_mixups(target_augmentations)

    augmented_targets: AugmentedTargets = []
    for mixup in mixups:
        augmentation_indices = get_augmentation_indices_for_mixup(target_augmentations, mixup)
        for target_index in range(len(target_files)):
            for augmentation_index in augmentation_indices:
                augmented_targets.append(AugmentedTarget(target_file_index=target_index,
                                                         target_augmentation_index=augmentation_index))

    return augmented_targets


def get_truth_indices_for_target(target: TargetFile) -> List[int]:
    """Get a list of truth indices for a given target."""
    index = [truth_setting.index for truth_setting in target.truth_settings]

    # flatten, uniquify, and sort
    return sorted(list(set([item for sublist in index for item in sublist])))


def get_truth_indices_for_augmented_target(augmented_target: AugmentedTarget, targets: TargetFiles) -> List[int]:
    return get_truth_indices_for_target(targets[augmented_target.target_file_index])


def get_mixup_for_augmented_target(augmented_target: AugmentedTarget, augmentations: Augmentations) -> int:
    return augmentations[augmented_target.target_augmentation_index].mixup


def get_target_indices_for_truth_index(targets: TargetFiles,
                                       truth_index: int,
                                       allow_multiple: bool = False) -> List[int]:
    """Get a list of target indices containing the given truth index.

    If allow_multiple is True, then include targets that contain multiple truth indices.
    """
    target_indices = set()
    for target_index, target in enumerate(targets):
        indices = get_truth_indices_for_target(target)
        if len(indices) == 1 or allow_multiple:
            for index in indices:
                if index == truth_index + 1:
                    target_indices.add(target_index)

    return sorted(list(target_indices))


def get_augmented_target_indices_for_truth_index(augmented_targets: AugmentedTargets,
                                                 targets: TargetFiles,
                                                 augmentations: Augmentations,
                                                 truth_index: int,
                                                 mixup: int,
                                                 allow_multiple: bool = False) -> List[int]:
    """Get a list of augmented target indices containing the given truth index.

    If allow_multiple is True, then include targets that contain multiple truth indices.
    """
    augmented_target_indices = set()
    for augmented_target_index, augmented_target in enumerate(augmented_targets):
        if get_mixup_for_augmented_target(augmented_target=augmented_target, augmentations=augmentations) == mixup:
            indices = get_truth_indices_for_augmented_target(augmented_target=augmented_target, targets=targets)
            if len(indices) == 1 or allow_multiple:
                for index in indices:
                    if index == truth_index + 1:
                        augmented_target_indices.add(augmented_target_index)

    return sorted(list(augmented_target_indices))


def get_augmented_target_indices_by_class(mixdb: MixtureDatabase,
                                          augmented_targets: AugmentedTargets,
                                          mixup: int) -> List[List[int]]:
    num_classes = mixdb.num_classes
    if mixdb.truth_mutex:
        num_classes -= 1

    indices = []
    for idx in range(num_classes):
        indices.append(
            get_augmented_target_indices_for_truth_index(augmented_targets=augmented_targets,
                                                         targets=mixdb.targets,
                                                         augmentations=mixdb.target_augmentations,
                                                         truth_index=idx,
                                                         mixup=mixup))
    return indices


def get_augmented_target_indices_for_mixup(mixdb: MixtureDatabase,
                                           augmented_targets: AugmentedTargets,
                                           mixup: int) -> List[List[int]]:
    from collections import deque
    from random import shuffle

    from sonusai import SonusAIError

    mixup_indices = []

    if mixup == 1:
        for index, augmented_target in enumerate(augmented_targets):
            if get_mixup_for_augmented_target(augmented_target=augmented_target,
                                              augmentations=mixdb.target_augmentations) == 1:
                mixup_indices.append([index])
        return mixup_indices

    augmented_target_indices_by_class = get_augmented_target_indices_by_class(mixdb=mixdb,
                                                                              augmented_targets=augmented_targets,
                                                                              mixup=mixup)

    if mixup > mixdb.num_classes:
        raise SonusAIError(
            f'Specified mixup, {mixup}, is greater than the number of classes, {mixdb.num_classes}')

    de = deque()

    # Keep looping until not enough targets remain for mixup
    while sum([1 for x in augmented_target_indices_by_class if x]) >= mixup:
        # Need more class indices?
        if len(de) < mixup:
            # Only choose classes that still have data
            counts = [len(item) for item in augmented_target_indices_by_class]
            # Need to subtract out indices already in the deque
            for idx in de:
                counts[idx] -= 1
            indices = [idx for idx, val in enumerate(counts) if val > 0]
            shuffle(indices)
            # Keep shuffling if the deque is not empty and the first new index matches the last item
            # (so that a class does not appear twice in a mixup)
            while de and indices[0] == de[-1]:
                shuffle(indices)
            for index in indices:
                de.append(index)

        class_indices = [de.popleft() for _ in range(mixup)]

        target_indices = []
        for class_index in class_indices:
            target_indices.append(augmented_target_indices_by_class[class_index].pop())

        mixup_indices.append(target_indices)

    return mixup_indices
