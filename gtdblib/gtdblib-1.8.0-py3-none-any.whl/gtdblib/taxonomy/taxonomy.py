import sys
from typing import Dict, List

from gtdblib import log
from gtdblib.taxon.taxon import Taxon
from gtdblib.taxon.rank import TaxonRank
from gtdblib.util.types import is_float
from gtdblib.utilshell.gtdbshutil import check_file_exists
from gtdblib.util.bio.accession import canonical_gid


def read_taxonomy(taxonomy_file: str, use_canonical_gid: bool = False) -> Dict[str, List[str]]:
    """Read Greengenes-style taxonomy file.

    This method is generic in that it can read any Greengenes-style taxonomy string
    and does not strictly require there to be the seven canonical ranks present.

    Expected format is:
        <accession>\t<taxonomy string>

    where the taxonomy string will typically have the formats:
        d__; c__; o__; f__; g__; s__

    :param taxonomy_file: File indicating Greengenes-style taxonomic assignments.
    :param use_canonical_gid: Flag indicating if accessions should be converted to their canonical form.
    :return: Mapping from accessions to a list of taxa.
    """

    check_file_exists(taxonomy_file)

    try:
        d = {}
        for row, line in enumerate(open(taxonomy_file)):
            line_split = line.split('\t')
            unique_id = line_split[0]

            if use_canonical_gid:
                unique_id = canonical_gid(unique_id)

            tax_str = line_split[1].rstrip()
            if tax_str[-1] == ';':
                # remove trailing semicolons which sometimes
                # appear in Greengenes-style taxonomy files
                tax_str = tax_str[0:-1]

            d[unique_id] = [x.strip() for x in tax_str.split(';')]
    except:
        log.error(f'Failed to parse taxonomy file on line {row+1}.')
        raise

    return d


def fill_trailing_ranks(taxa: List[str]) -> List[str]:
    """Fill in missing trailing ranks in a taxonomy string.

    This function assumes it will be provided with a list
    of taxa from the 7 canonical ranks in rank order. Any
    trailing ranks are filled in.

    Example: [d__Bacteria, d__Firmicutes] => [d__Bacteria, d__Firmicutes, c__, o__, f__, g__, s__]

    :param taxa list: List of taxa.

    :return: List of taxa with filled trailing ranks.
    """

    if not taxa:
        return ';'.join(TaxonRank.RANK_PREFIXES)

    try:
        last_rank = Taxonomy.RANK_PREFIXES.index(taxa[-1][0:3])
    except:
        log.error('Taxon is missing rank prefix: %s' % ';'.join(taxa))
        sys.exit()

    for i in range(last_rank+1, len(Taxonomy.RANK_PREFIXES)):
        taxa.append(Taxonomy.RANK_PREFIXES[i])

    return taxa


def read_taxonomy_from_tree(tree: str, warnings: bool = True) -> Dict[str, List[str]]:
    """Obtain the taxonomy for each extant taxa as specified by internal tree labels.

    This method is generic in that it can read any Greengenes-style taxonomy string
    and does not strictly require extran taxa to be classified to theseven canonical ranks.

    :param tree: Filename of Newick tree or Dendropy tree object.
    :param warnings: Flag indicating if issues reading tree should be logged as warnings.

    :return: Mapping from extent taxon labels to a list of taxa.
    """

    if isinstance(tree, str):
        import dendropy
        tree = dendropy.Tree.get_from_path(tree,
                                           schema='newick',
                                           rooting="force-rooted",
                                           preserve_underscores=True)

    taxonomy = {}
    for leaf in tree.leaf_node_iter():
        taxa = []

        node = leaf.parent_node
        while node:
            if node.label:
                taxa_str = node.label
                if ':' in taxa_str:
                    taxa_str = taxa_str.split(':')[1]

                if not is_float(taxa_str):
                    if taxa_str[-1] == ';':
                        taxa_str = taxa_str[:-1]

                    # check for concatenated ranks of the form: p__Crenarchaeota__c__Thermoprotei
                    for prefix in Taxonomy.rank_prefixes:
                        split_str = '__' + prefix
                        if split_str in taxa_str:
                            taxa_str = taxa_str.replace(
                                split_str, ';' + prefix)

                    # appears to be an internal label and not simply a support value
                    taxa = [x.strip() for x in taxa_str.split(';')] + taxa
            node = node.parent_node

        if warnings and len(taxa) > len(TaxonRank.RANK_LABELS):
            log.warning('Invalid taxonomy string read from tree for taxon {}: {}'.format(
                leaf.taxon.label,
                ';'.join(taxa)))

        # check if genus name should be appended to species label as some trees
        # indicate species only by their specific epithet
        if len(taxa) == len(TaxonRank.RANK_LABELS):
            genus = taxa[5][3:]
            species = taxa[6][3:]
            if genus not in species and len(species.split()) == 1:
                taxa[6] = 's__' + genus + ' ' + species

        taxa = fill_trailing_ranks(taxa)
        taxonomy[leaf.taxon.label] = taxa

    return taxonomy


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
