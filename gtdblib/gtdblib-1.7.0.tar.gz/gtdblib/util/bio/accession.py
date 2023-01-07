import re

RE_CANONICAL = re.compile(r'^(?:GB_)?(?:RS_)?(?:GCF_)?(?:GCA_)?(\d{9})\.\d')


def canonical_gid(gid: str) -> str:
    """Get canonical form of NCBI genome accession.

    Example:
        G005435135 -> G005435135
        GCF_005435135.1 -> G005435135
        GCF_005435135.1_ASM543513v1_genomic -> G005435135
        RS_GCF_005435135.1 -> G005435135
        GB_GCA_005435135.1 ->

    :param gid: Genome accesion to conver to canonical form.
    :return: Canonical form of accession.
    """

    match = RE_CANONICAL.match(gid)
    if match:
        return f'G{match[1]}'
    else:
        return gid


def is_same_accn_version(accn1: str, accn2: str) -> bool:
    """Check if accessions have same version number.

    This method assumes accession versions are provided
    as a suffix proceeding a period. This is the format
    used for NCBI accessions, e.g. GCF_005435135.1.

    :param accn1: First accession.
    :param accn2: Second accession.
    :return: True if version number is the same, else False.
    """

    return int(accn1.split('.')[1]) == int(accn2.split('.')[1])
