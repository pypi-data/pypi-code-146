from typing import Tuple, Optional

from gtdblib.util.types import is_float


def parse_label(label: str) -> Tuple[Optional[float], Optional[str], Optional[str]]:
    """Parse a Newick label which may contain a support value, taxon, and/or auxiliary information.

    :param label: The label to parse.
    :returns: A tuple containing the support value, taxon, and auxiliary information.
    """

    support = None
    taxon = None
    auxiliary_info = None

    if label:
        label = label.strip()
        if '|' in label:
            label, auxiliary_info = label.split('|', 1)

        if ':' in label:
            support, taxon = label.split(':')
            support = float(support)
        else:
            if is_float(label):
                support = float(label)
            elif label != '':
                taxon = label

    return support, taxon, auxiliary_info


def create_label(support: Optional[float], taxon: Optional[str], auxiliary_info: Optional[str]) -> str:
    """Create label for Newick tree.

    :param support: The support value.
    :param taxon: The taxon.
    :param auxiliary_info: The auxiliary information.
    """

    label = ''
    if support is not None and taxon:
        label = str(support) + ':' + taxon
    elif support is not None:
        label = str(support)
    elif taxon:
        label = taxon

    if auxiliary_info:
        label += '|' + auxiliary_info

    return label
