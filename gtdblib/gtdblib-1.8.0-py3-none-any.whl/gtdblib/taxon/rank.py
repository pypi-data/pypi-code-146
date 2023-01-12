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

    RANK_PREFIXES = ('d__', 'p__', 'c__', 'o__', 'f__', 'g__', 's__')
    RANK_LABELS = ('domain', 'phylum', 'class', 'order',
                   'family', 'genus', 'species')
    RANK_INDEX = {'d__': 0, 'p__': 1, 'c__': 2,
                  'o__': 3, 'f__': 4, 'g__': 5, 's__': 6}

    DOMAIN_INDEX = 0
    PHYLUM_INDEX = 1
    CLASS_INDEX = 2
    ORDER_INDEX = 3
    FAMILY_INDEX = 4
    GENUS_INDEX = 5
    SPECIES_INDEX = 6
