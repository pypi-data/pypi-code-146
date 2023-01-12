from gtdblib.taxon.rank import TaxonRank


class Taxon:
    __slots__ = ('rank', 'value')

    def __init__(self, rank: TaxonRank, value: str):
        self.rank: TaxonRank = rank
        self.value = value
