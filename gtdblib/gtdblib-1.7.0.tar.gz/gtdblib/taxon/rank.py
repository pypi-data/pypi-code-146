from enum import Enum


class TaxonRank(Enum):
    """A taxonomic rank (e.g. Domain, Phylum, etc...)."""

    DOMAIN = 'd__'
    PHYLUM = 'p__'
    CLASS = 'c__'
    ORDER = 'o__'
    FAMILY = 'f__'
    GENUS = 'g__'
    SPECIES = 's__'
