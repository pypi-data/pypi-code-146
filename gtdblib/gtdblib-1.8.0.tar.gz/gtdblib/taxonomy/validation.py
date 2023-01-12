"""Methods for validating a Greengenes-style taxonomy.

This class validates canonical 7 rank Greengenes-style taxonomy string:
    d__; c__; o__; f__; g__; s__
"""

import re
from collections import defaultdict
from typing import Dict, List, Tuple

from gtdblib import log
from gtdblib.taxon.rank import TaxonRank


def validate_taxonomy(
        taxonomy: Dict[str, List[str]],
        check_prefixes: bool,
        check_ranks: bool,
        check_hierarchy: bool,
        check_species: bool,
        check_group_names: bool,
        check_duplicate_names: bool,
        check_capitalization: bool,
        report_errors: bool = True) -> Tuple[Dict[str, str], Dict[str, str], Dict[str, List[str]], Dict[str, List[str]]]:
    """Check if taxonomy forms a strict hierarchy with all expected ranks.

    This method implements a full workflow for validating Greengenes-style taxonomy strings assigned
    to a set of accessions. It identifies a number of common issues and the issues checked can be
    configured using the set of boolean inputs.

    Parameters
    ----------
    taxonomy : d[unique_id] -> [d__<taxon>; ...; s__<taxon>]
        Taxonomy strings indexed by unique ids.
    check_prefixes : boolean
        Flag indicating if prefix of taxon should be validated.
    check_ranks : boolean
        Flag indicating if the presence of all ranks should be validated.
    check_hierarchy : boolean
        Flag indicating if the taxonomic hierarchy should be validated.
    check_species : boolean
        Flag indicating if the taxonomic consistency of named species should be validated.
    check_group_names : boolean
        Flag indicating if group names should be checked for invalid characters.
    check_duplicate_names : boolean
        Flag indicating if group names should be checked for duplicates.
    report_errors : boolean
        Flag indicating if errors should be written to screen.

    Returns
    -------
    dict : d[taxon_id] -> taxonomy
        Taxa with invalid number of ranks.
    dict : d[taxon_id] -> [taxon, taxonomy]
        Taxa with invalid rank prefixes.
    dict: d[taxon_id] -> [species name, error message]
        Taxa with invalid species names.
    dict: d[child_taxon_id] -> two or more parent taxon ids
        Taxa with invalid hierarchies.
    """

    # check for incomplete taxonomy strings or unexpected rank prefixes
    try:
        invalid_ranks = {}
        invalid_prefixes = {}
        invalid_species_name = {}
        invalid_group_name = {}
        invalid_capitalization = set()
        for taxon_id, taxa in taxonomy.items():
            if check_ranks:
                if len(taxa) != len(TaxonRank.RANK_PREFIXES):
                    invalid_ranks[taxon_id] = ';'.join(taxa)
                    continue

            if check_prefixes:
                for r, taxon in enumerate(taxa):
                    if taxon[0:3] != TaxonRank.RANK_PREFIXES[r]:
                        invalid_prefixes[taxon_id] = [taxon, ';'.join(taxa)]
                        break

            if check_group_names:
                for taxon in taxa:
                    canonical_taxon = ' '.join(
                        [t.strip() for t in re.split('_[A-Z]+(?= |$)', taxon[3:])]).strip()
                    if canonical_taxon and re.match('^[a-zA-Z0-9- ]+$', canonical_taxon) is None:
                        if not taxon.startswith('s__') or check_species:
                            invalid_group_name[taxon_id] = [
                                taxon, 'Taxon contains invalid characters']

            if check_species:
                genus_index = TaxonRank.RANK_INDEX['g__']
                species_index = TaxonRank.RANK_INDEX['s__']
                if len(taxa) > species_index:
                    species_name = taxa[species_index]
                    valid, error_msg = validate_species_name(
                        species_name, require_full=True, require_prefix=True)
                    if not valid:
                        invalid_species_name[taxon_id] = [
                            species_name, error_msg]

                    if species_name != 's__':
                        genus_name = taxa[genus_index]
                        generic_name = species_name.split()[0]
                        if genus_name[3:] != generic_name[3:]:
                            invalid_species_name[taxon_id] = [
                                species_name, 'Genus and generic names do not match: %s' % genus_name]

            if check_capitalization:
                for taxon in taxa:
                    if len(taxon) > 3 and taxon[3].islower():
                        invalid_capitalization.add(taxon)
    except:
        log.error(
            'Exception raised while processing {} with the taxa set {}'.format(taxon_id, taxa))
        raise

    # check for duplicate names
    invalid_duplicate_name = []
    if check_duplicate_names:
        invalid_duplicate_name = duplicate_names(taxonomy, check_species)

    # check for inconsistencies in the taxonomic hierarchy
    invalid_hierarchies = defaultdict(set)
    missing_parent = set()
    if check_hierarchy:
        expected_parent = taxonomic_consistency(taxonomy, False)

        for taxon_id, taxa in taxonomy.items():
            for r in range(1, len(taxa)):
                if len(taxa[r]) == 3:
                    continue

                if r == TaxonRank.RANK_INDEX['s__'] and not check_species:
                    continue

                if taxa[r] not in expected_parent:
                    missing_parent.add(taxa[r])
                elif taxa[r - 1] != expected_parent[taxa[r]]:
                    invalid_hierarchies[taxa[r]].add(taxa[r - 1])
                    invalid_hierarchies[taxa[r]].add(expected_parent[taxa[r]])

    if report_errors:
        if len(invalid_ranks):
            print('')
            print('Taxonomy contains too few ranks:')
            for taxon_id, taxa_str in invalid_ranks.items():
                print('%s\t%s' % (taxon_id, taxa_str))

        if len(invalid_prefixes):
            print('')
            print('Taxonomy contains an invalid rank prefix:')
            for taxon_id, info in invalid_prefixes.items():
                print('%s\t%s\t%s' % (taxon_id, info[0], info[1]))

        if len(invalid_group_name):
            print('')
            print('Taxa containing invalid characters:')
            for taxon_id, err_msg in invalid_group_name.items():
                print('%s\t%s\t%s' % (taxon_id, err_msg[0], err_msg[1]))

        if len(invalid_species_name):
            print('')
            print('Taxonomy contains invalid species names:')
            for taxon_id, info in invalid_species_name.items():
                print('%s\t%s\t%s' % (taxon_id, info[0], info[1]))

        if len(invalid_duplicate_name):
            print('')
            print('Taxonomy contains identical taxon names in multiple lineages:')
            for duplicate_name in invalid_duplicate_name.keys():
                print('%s' % duplicate_name)

        if len(missing_parent):
            print('')
            print('Taxonomy contains taxa with an undefined parent:')
            for taxon in missing_parent:
                print('%s' % taxon)

        if len(invalid_hierarchies):
            print('')
            print('Taxonomy contains taxa with multiple parents:')
            for child_taxon, parent_taxa in invalid_hierarchies.items():
                print('%s\t%s' % (child_taxon, ', '.join(parent_taxa)))

        if len(invalid_capitalization):
            print('')
            print('Taxa do not start with a capital letter:')
            for taxon in invalid_capitalization:
                print('{}'.format(taxon))

    return invalid_ranks, invalid_prefixes, invalid_species_name, invalid_hierarchies, invalid_group_name, invalid_capitalization


def duplicate_names(taxonomy: Dict[str, List[str]], check_species: bool = True) -> Dict[str, List[str]]:
    """Identify duplicate names in taxonomy.

    Parameters
    ----------
    taxonomy : d[unique_id] -> [d__<taxon>; ...; s__<taxon>]
        Taxonomy strings indexed by unique ids.

    Returns
    -------
    dict : d[taxon] -> lineages
        List of lineages for duplicate taxa.
    """

    # get lineages for each taxon name
    taxon_lineages = defaultdict(set)
    for taxa in taxonomy.values():
        for i, taxon in enumerate(taxa):
            if len(taxon) > 3:
                taxon_lineages[taxon].add(';'.join(taxa[0:i+1]))

    # identify taxon belonging to multiple lineages
    duplicates = {}
    for taxon, lineages in taxon_lineages.items():
        if len(lineages) >= 2:
            if not taxon.startswith('s__') or check_species:
                duplicates[taxon] = lineages

    return duplicates


def validate_species_name(species_name: str, require_full: bool = True, require_prefix: bool = True) -> Tuple[bool, str]:
    """Validate species name.

    A full species name should be  binomial and include a 'generic name' (genus) and
    a 'specific epithet' (species), i.e. Escherichia coli. This method
    assumes the two names should be separated by a space.

    Parameters
    ----------
    species_name : str
        Species name to validate
    require_full : boolean
        Flag indicating if species name must include 'generic name and 'specific epithet'.
    require_prefix : boolean
        Flag indicating if name must start with the species prefix ('s__').

    Returns
    -------
    boolean
        True if species name is valid, otherwise False.
    str
        Reason for failing validation, otherwise None.
    """

    if species_name == 's__':
        return True, None

    # test for prefix
    if require_prefix:
        if not species_name.startswith('s__'):
            return False, 'name is missing the species prefix'

    # remove prefix before testing other properties
    test_name = species_name
    if test_name.startswith('s__'):
        test_name = test_name[3:]

    # test for full name
    if require_full:
        if 'candidatus' in test_name.lower():
            if len(test_name.split(' ')) <= 2:
                return False, 'name appears to be missing the generic name'
        else:
            if len(test_name.split(' ')) <= 1:
                return False, 'name appears to be missing the generic name'

    # check for tell-tale signs on invalid species names
    if " bacterium" in test_name.lower():
        return False, "name contains the word 'bacterium'"
    if " archaeon" in test_name.lower():
        return False, "name contains the word 'archaeon'"
    if " archeaon" in test_name.lower():
        return False, "name contains the word 'archeaon'"
    if "-like" in test_name.lower():
        return False, "name contains '-like'"
    if " group " in test_name.lower():
        return False, "name contains 'group'"
    if " symbiont" in test_name.lower():
        return False, "name contains 'symbiont'"
    if " endosymbiont" in test_name.lower():
        return False, "name contains 'endosymbiont'"
    if " taxon" in test_name.lower():
        return False, "name contains 'taxon'"
    if " cluster" in test_name.lower():
        return False, "name contains 'cluster'"
    if " of " in test_name.lower():
        return False, "name contains 'of'"
    if test_name[0].islower():
        return False, 'first letter of name is lowercase'
    if 'sp.' in test_name.lower():
        return False, "name contains 'sp.'"

    return True, None


def taxonomic_consistency(taxonomy: Dict[str, List[str]], report_errors: bool = True) -> Dict[str, str]:
    """Determine taxonomically consistent classification for taxa at each rank.

    Parameters
    ----------
    taxonomy : d[unique_id] -> [d__<taxon>; ...; s__<taxon>]
        Taxonomy strings indexed by unique ids.
    report_errors : boolean
        Flag indicating if errors should be written to screen.

    Returns
    -------
    dict : d[taxa] -> expected parent
        Expected parent taxon for taxa at all taxonomic ranks, or
        None if the taxonomy is inconsistent.
    """

    expected_parent = {}
    for genome_id, taxa in taxonomy.items():
        if taxa[0] == 'd__Viruses' or '[P]' in taxa[0]:
            # *** This is a HACK. It would be far better to enforce
            # a taxonomically consistent taxonomy, but
            # the viral taxonomy at IMG is currently not consistent
            continue

        for r in range(1, len(taxa)):
            if len(taxa[r]) == 3:
                break

            if taxa[r] in expected_parent:
                if report_errors:
                    if taxa[r - 1] != expected_parent[taxa[r]]:
                        log.warning(
                            'Provided taxonomy is not taxonomically consistent.')
                        log.warning('Genome %s indicates the parent of %s is %s.' % (
                            genome_id, taxa[r], taxa[r - 1]))
                        log.warning('The parent of this taxa was previously indicated as %s.' % (
                            expected_parent[taxa[r]]))

            expected_parent[taxa[r]] = taxa[r - 1]

    return expected_parent
