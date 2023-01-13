# File Name: gtf.py
# Created By: ZW
# Created On: 2022-12-20
# Purpose: defines class for gtf style objects (identical to the GFF2 spec),
#  as defined by standards at https://genome.ucsc.edu/FAQ/FAQformat.html#format3

# module imports
# ----------------------------------------------------------------------------
from dataclasses import dataclass
from operator import lt, gt
from re import split as re_split
from re import match
from typing import Union

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

# function check_and_convert_nums() takes a string and converts it to 
# a floating point python number if it looks like an integer or float,
# otherwise, it returns the string back unchanged
def check_and_convert_nums(string):
    pattern = "^[+-]?((\d+(\.\d+)?)|(\.\d+))$"
    mth = match(pattern, string)
    return (float(mth.string) if mth is not None else string)

# class definitions
# ----------------------------------------------------------------------------

# class Gtf() - base class for all GTF-type gene-like objects. 
# * indexing of genomic intervals follow GTF conventions. This means that
#   chromosome scaffolds begin at base 1. (This differs from bed-syle so care
#   must be taken when intersecting the two object types) the end of the interval
#   is inclusive [chromStart, chromEnd], creating slightly different intersection
#   rules than bed-style objects. 
#
# * The Gtf class contains nine attributes: 
#     1. chrom - chromosome of the feature
#     2. source - The program that generated this feature
#     3. feature - The name of the type of feature e.g. (exon, transcript, CDS, etc. )
#     4. chromStart - chromosome start position [ 1-indexed, inclusive ]
#     5. chromEnd - chromosome end position [ 1-indexed, inclusive ]
#     6. score - A score between 0 and 1000, can be used for filtering or visual cues
#     7. strand - strand options include "+", "-", or "." (for don't know/don't care)
#     8. frame - for exons and similar, frame should be a number between 0-2
#     9. attributes -  raw string representing attribute list. converted and stored in 
#           attr_dict for convenience of use and filtering.
@dataclass
class Gtf:
    chrom: str
    source: str  # e.g. HAVANA, ncbi, etc
    feature: str 
    chromStart: int # 1-indexed, beware interfacing with BED objects
    chromEnd: int # 1-indexed, inclusive, beware interfacing with BED objects
    score: float  # 0-1000 
    strand: str  # '+', '-', or '.'
    frame: Union[str,int]  # 0-2 or '.'
    attributes: str  # raw string repr of the attributes, converted below
    
    # define post_init routines to create attribute dictionary
    def __post_init__(self): # TODO
        self.chromStart = int(self.chromStart)
        self.chromEnd = int(self.chromEnd)
        self.score = check_and_convert_nums(str(self.score))
        self.zero_idx_start = self.chromStart - 1  # always inclusive
        self.zero_idx_end = self.chromEnd - 1  #always inclusive

        # handle attributes field
        self.attr_dict = {}
        pre_proc_attr = self.attributes.split("; ")
        if pre_proc_attr != ['']:
            for pair in pre_proc_attr:
                k,v = [p.strip('"') for p in pair.strip(";").split()]
                if k not in self.attr_dict.keys():
                    self.attr_dict[k] = [check_and_convert_nums(v)]
                else:
                    self.attr_dict[k].append(check_and_convert_nums(v))

    # define custom representation when printing the GTF object
    def __repr__(self):
        spec = (
            f" {self.chrom} {self.source} {self.feature}"
            f" {self.chromStart} {self.chromEnd} {self.score}"
            f" {self.strand} {self.frame} {self.attributes} "
        )
        return repr(f"Gtf({spec})")

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
