from gtdblib.taxon.taxon import Taxon


class Taxonomy:
    __slots__ = ('d', 'p', 'c', 'o', 'f', 'g', 's')

    def __init__(self, d: Taxon, p: Taxon, c: Taxon, o: Taxon, f: Taxon, g: Taxon, s: Taxon):
        self.d = d
        self.p = p
        self.c = c
        self.o = o
        self.f = f
        self.g = g
        self.s = s
