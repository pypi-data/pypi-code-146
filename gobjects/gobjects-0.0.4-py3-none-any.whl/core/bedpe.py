# File Name: bedpe.py
# Created By: ZW
# Created On: 2022-01-10
# Purpose: defines class for bedpe style objects (identical to the Bedtools BEDPE spec),
#  as defined by standards at https://bedtools.readthedocs.io/en/latest/content/general-usage.html

# module imports
# ----------------------------------------------------------------------------
from .bed import Bed6
from dataclasses import dataclass
from operator import lt, gt
from re import split as re_split
from re import match


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

# class Bedpe() - base class for all Bedpe-type objects which can be used for 
# storing paired-end style objects or long-range interactions like those created
# by promoter-capture HiC. 
# * indexing of genomic intervals follow BED conventions. This means that
#   chromosome scaffolds begin at base 0. (This differs from gtf-syle so care
#   must be taken when intersecting the two object types) the end of the interval
#   is exclusive [chromStart, chromEnd), creating slightly different intersection
#   rules than bed-style objects. 
#
# * The Bedpe class contains nine attributes: 
#     1. chrom - chromosome of first interval
#     2. chromStart - chromosome start position for first interval [ 0-indexed, exclusive ]
#     3. chromEnd - chromosome end position for first interval [ 0-indexed, exclusive ]
#     4. chrom2 - chromosome of second interval
#     5. chromStart2 - chromosome start position for second interval [ 0-indexed, exclusive ]
#     6. chromEnd2 - chromosome end position for second interval [ 0-indexed, exclusive ]    
#     7. name - name of the feature
#     8. score - A score between 0 and 1000, can be used for filtering or visual cues
#     9. strand1 - strand for first interval | "+", "-", or "." (for don't know/don't care)
#     10. strand2 - strand for first interval | "+", "-", or "." (for don't know/don't care)
#     11. attributes -  raw string representing attribute list. converted and stored in 
#           attr_dict for convenience of use and filtering. should mirror format of GTF
@dataclass
class Bedpe:
    # raw information from object
    chrom1: str
    chromStart1: int # 0-indexed, beware interfacing with GTF objects
    chromEnd1: int # 0-indexed, inclusive, beware interfacing with GTF objects
    chrom2: str
    chromStart2: int # 0-indexed, beware interfacing with GTF objects
    chromEnd2: int # 0-indexed, inclusive, beware interfacing with GTF objects
    name: str
    score: float  # 0-1000 
    strand1: str  # '+', '-', or '.'
    strand2: str  # '+', '-', or '.'
    attributes: str  # raw string repr of the attributes, converted below

    # define post_init routines to create internal Bed6 objects for each
    # interval as well as an attribute dictionary shared between the two
    def __post_init__(self): # TODO
        self.bed1 = Bed6(
            self.chrom1, self.chromStart1, self.chromEnd1,
            self.name, self.score, self.strand1
        )
        self.bed2 = Bed6(
            self.chrom2, self.chromStart2, self.chromEnd2,
            self.name, self.score, self.strand2
        )

        # precompute first and second bed intervals in sort order to lessen
        # comparison burden in intersection and sorting operations
        self.first_bed = min([self.bed1,self.bed2])
        self.second_bed = max([self.bed1, self.bed2])

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

    # define custom representation when printing the Bedpe object
    def __repr__(self):
        spec = (
            f" {self.bed1} {self.bed2}"
            f" {self.attributes} "
        )
        return repr(f"Bedpe({spec})")

    # define a custom function for the equal to (==) comparator
    # based on identical interval information on matching coordinates
    def __eq__(self, other):
        comp = (((self.bed1 == other.bed1) and (self.bed2 == other.bed2)) or 
            ((self.bed1 == other.bed2) and (self.bed2 == other.bed1)))
        return comp
    
    # define a custom function for the (<) comparator. For Bedpe objects,
    # we define less than as the minimum of the two paired intervals 
    # compared to the minimum of the two paired intervals of the other object. 
    # if the minimum interval is identical, we compare the other interval from each 
    # This comparison only works for Bedpe to Bedpe objects.
    def __lt__(self, other):
        if lt(*[prep_chrom_comp(c) for c in [self.first_bed.chrom, other.first_bed.chrom]]): return True
        elif gt(*[prep_chrom_comp(c) for c in [self.first_bed.chrom, other.first_bed.chrom]]): return False
        else: # if the chromosomes names are equal by natural sort
            comp = ((self.first_bed < other.first_bed) or 
                    ((self.first_bed == other.first_bed) and 
                    (self.second_bed < other.second_bed)))
            return comp

    # define a custom function for the (>) comparator. For Bedpe objects,
    # we define greater than as the minimum of the two paired intervals 
    # compared to the minimum of the two paired intervals of the other object. 
    # This comparison only works for Bedpe to Bedpe objects.
    def __gt__(self, other):
        if lt(*[prep_chrom_comp(c) for c in [self.first_bed.chrom, other.first_bed.chrom]]): return False
        elif gt(*[prep_chrom_comp(c) for c in [self.first_bed.chrom, other.first_bed.chrom]]): return True
        else: # if the chromosomes names are equal by natural sort
            comp = ((self.first_bed > other.first_bed) or 
                    ((self.first_bed == other.first_bed) and 
                    (self.second_bed > other.second_bed)))
            return comp

    # define a custom function for the (<=) comparator. See __lt__ , __gt__ ,
    # and __eq__ as implemented above for specifics
    def __le__(self, other):
        return (self.__lt__(other) or self.__eq__(other))

    # define a custom function for the (>=) comparator. See __lt__ , __gt__ ,
    # and __eq__ as implemented above for specifics
    def __ge__(self,other):
        return (self.__gt__(other) or self.__eq__(other))
