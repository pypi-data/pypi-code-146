from sonusai.mixture.mixdb import MixtureDatabase
from sonusai.mixture.types import AugmentedTargets


def balance_targets(mixdb: MixtureDatabase, augmented_targets: AugmentedTargets) -> AugmentedTargets:
    import numpy as np

    from sonusai.mixture import get_mixups
    from sonusai.mixture import AugmentedTarget
    from sonusai.mixture import get_augmented_target_indices_by_class

    if not mixdb.class_balancing:
        return augmented_targets

    mixups = get_mixups(mixdb.target_augmentations)
    if 1 in mixups:
        mixups.remove(1)

    for mixup in mixups:
        augmented_target_indices_by_class = get_augmented_target_indices_by_class(
            mixdb=mixdb,
            augmented_targets=augmented_targets,
            mixup=mixup)

        largest = max([len(item) for item in augmented_target_indices_by_class])
        largest = int(np.ceil(np.float32(largest) / mixup)) * mixup
        for at_indices in augmented_target_indices_by_class:
            additional_augmentations_needed = largest - len(at_indices)
            target_file_indices = sorted(
                list(set([augmented_targets[at_index].target_file_index for at_index in at_indices])))

            tfi_idx = 0
            for _ in range(additional_augmentations_needed):
                target_file_index = target_file_indices[tfi_idx]
                tfi_idx = (tfi_idx + 1) % len(target_file_indices)
                augmentation_index = _get_unused_balancing_augmentation(mixdb=mixdb,
                                                                        augmented_targets=augmented_targets,
                                                                        target_file_index=target_file_index,
                                                                        mixup=mixup)
                augmented_target = AugmentedTarget(target_file_index=target_file_index,
                                                   target_augmentation_index=augmentation_index)
                augmented_targets.append(augmented_target)

    return augmented_targets


def _get_unused_balancing_augmentation(mixdb: MixtureDatabase,
                                       augmented_targets: AugmentedTargets,
                                       target_file_index: int,
                                       mixup: int) -> int:
    """Get an unused balancing augmentation for a given target file index."""
    from dataclasses import asdict

    from sonusai.mixture import get_augmentations
    from sonusai.mixture import get_class_balancing_augmentation

    balancing_augmentations = [item for item in range(len(mixdb.target_augmentations)) if
                               item >= mixdb.first_cba_index]
    used_balancing_augmentations = [at.target_augmentation_index for at in augmented_targets if
                                    at.target_file_index == target_file_index and
                                    at.target_augmentation_index in balancing_augmentations]

    augmentation_indices = [item for item in balancing_augmentations if
                            item not in used_balancing_augmentations and
                            mixdb.target_augmentations[item].mixup == mixup]
    class_balancing_augmentation = get_class_balancing_augmentation(mixdb=mixdb,
                                                                    target_file_index=target_file_index)
    if len(augmentation_indices) == 0:
        new_augmentation = get_augmentations(rules=asdict(class_balancing_augmentation),
                                             num_ir=len(mixdb.ir_files))[0]
        new_augmentation.mixup = mixup
        mixdb.target_augmentations.append(new_augmentation)
        augmentation_indices.append(len(mixdb.target_augmentations) - 1)

    return augmentation_indices[0]
