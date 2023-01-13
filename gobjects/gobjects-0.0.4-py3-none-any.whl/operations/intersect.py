# File Name: intersect.py
# Created By: ZW
# Created On: 2022-12-22
# Purpose: define functions for interval algebra ( much like those found
#  in bedtools ) specifically bedtools intersect-like functionality.

# module imports
# ----------------------------------------------------------------------------
from ..core.bed import Bed6, Bed12
from ..core.bedpe import Bedpe
from ..core.gtf import Gtf
from ..core.intervals import Interval

# constants definitions
# ----------------------------------------------------------------------------
CONTIGUOUS = [Interval, Bed6, Bed12, Gtf]
NON_CONTIGUOUS = [Bedpe]
ALL_GOBJECTS = CONTIGUOUS + NON_CONTIGUOUS

# function definitions
# ----------------------------------------------------------------------------

# define check_stranded() which takes an object and ensures it contains the
# self.strand attribute. If it does, the function returns None, if it doesn't
# the function raises an Attribute error.
def check_stranded(gobj):
    if not hasattr(gobj, "strand"):
        msg = (
            "Error! attemped strand-aware comparison"
            " for object with no strand information"
            )
        raise AttributeError(msg)
    else:
        return None

# define intersect() which takes two contiguous features, like Bed or GTF
# and returns the boolean result of the interval intersect. the function
# has a strand-aware option but is not checked internally for strand attrs
def intersect(gobjA, gobjB, strand_aware=False):
    if not all((type(gobjA) in CONTIGUOUS, type(gobjB) in CONTIGUOUS)):
        raise TypeError(
            "Cannot perform intersect() on non-contiguous features.\n"
            f"please ensure {gobjB} and/or {gobjB}. are in {CONTIGUOUS}"
        )
    
    if strand_aware:  # check for strand information on strand aware items
        check_stranded(gobjA) 
        check_stranded(gobjB)
    
    if strand_aware and (gobjA.strand != gobjB.strand): return False
    else:  # regular intersect routine
        if gobjA.chrom != gobjB.chrom: return False
        else:
            return not (  # define NOT intersection conditions
                ((gobjA.zero_idx_end) < gobjB.zero_idx_start) or
                 (gobjA.zero_idx_start > (gobjB.zero_idx_end)))



