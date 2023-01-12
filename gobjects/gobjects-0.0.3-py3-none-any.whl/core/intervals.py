# File Name: intervals.py
# Created By: ZW
# Created On: 2022-11-03
# Purpose: defines base class for BED style intervals commonly
#  used to describe linear features in the genome.


# module imports
# ----------------------------------------------------------------------------
from dataclasses import dataclass
from operator import lt, gt
from re import split as re_split

# function definitions
# ----------------------------------------------------------------------------

# function prep_chrom_compare() splits contig names that are a combo of
# strings and digits to use as sorting keys in sort functions and similar 
# processes. for example: 'chr1' -> ('chr', 1). this function can be 
# used in the sorted() function with the key=prep_chrom_comp argument
def prep_chrom_comp(chrom: str):
    def recode(substr: str):
        return int(substr) if substr.isdigit() else substr.lower()
    return [recode(sub) for sub in re_split('([0-9]+)',chrom)]

# class definitions
# ----------------------------------------------------------------------------

# class Interval() - base class for all BED-type genome interval objects. 
# * indexing of genomic intervals follow BED conventions. This means that
#   chromosome scaffolds begin at base 0. the the end of the interval is 
#   equal to 1 + the feature end. this represents half-open intervals of the type
#   [chromStart, chromEnd), and but importantly, they represent 
#   chrom:(chromStart+1)-chromEnd intervals in position notation, for example:
#   chr1:1-1000 is equivalent to the Interval "chr1 0 1000" or chr1: [0,1000)
#
#  * the class contains only four attributes:
#     1. chromosome (chrom) -required- 
#     2. chromosome start position (chromEnd) -required-
#     3. chromosome end position (chromEnd) -required- 
#     4. feature name (name) -required-
@dataclass(eq=False, order=False)
class Interval():
    chrom: str
    chromStart: int
    chromEnd: int
    name: str

    # define a post-init method to coerce ints and floats properly
    def __post_init__(self):
        self.chromStart = int(self.chromStart)
        self.chromEnd = int(self.chromEnd)
        self.zero_idx_start = self.chromStart  # always inclusive
        self.zero_idx_end = self.chromEnd - 1  # always inclusive

    # define a custom printout representation for the Interval
    def __repr__(self):
        spec = f" {self.chrom} {self.chromStart} {self.chromEnd} {self.name} "
        return repr(f"Interval({spec})")
    
    # define a custom function for the equal to (==) comparator
    # based on identical interval information on matching coordinates
    def __eq__(self, other):
        comp = ((self.chrom == other.chrom) and
                (self.chromStart == other.chromStart) and
                (self.chromEnd == other.chromEnd))
        return comp
    
    # define a custom function for the less than (<) comparator
    # based on interval algebra on matching chromosomes
    def __lt__(self, other):
        if lt(*[prep_chrom_comp(c) for c in [self.chrom, other.chrom]]): return True
        elif gt(*[prep_chrom_comp(c) for c in [self.chrom, other.chrom]]): return False
        else: # if the chromosomes names are equal by natural sort
            comp = ((self.chromStart < other.chromStart) or
                    ((self.chromStart == other.chromStart) and
                    (self.chromEnd < other.chromEnd)))
            return comp
    
    # define a custom function for the greater than (>) comparator
    # based on interval algebra on matching chromosomes
    def __gt__(self, other):
        if lt(*[prep_chrom_comp(c) for c in [self.chrom, other.chrom]]): return False
        elif gt(*[prep_chrom_comp(c) for c in [self.chrom, other.chrom]]): return True
        else: # if the chromosomes names are equal by natural sort
            comp = ((self.chromStart > other.chromStart) or 
                    ((self.chromEnd == other.chromEnd) and
                    (self.chromStart > other.chromStart)))
            return comp
    
    # define a custom function for the less than or equal to (<=) comparator
    # based on niterval algebra on matching chromosomes
    def __le__(self,other):
        return (self.__lt__(other) or self.__eq__(other))
    
    # define a custom function for the greater than or equal to (>=) comparator
    # based on interval algebra on matching chromosomes
    def __ge__(self,other):
        return (self.__gt__(other) or self.__eq__(other))
    
