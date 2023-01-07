from pathlib import Path

import dendropy
from rich.progress import track

from gtdblib import log
from gtdblib.util.bio.accession import canonical_gid


def convert_tree_accessions_to_canonical(input_path: Path, output_path: Path):
    """Convert all accessions a tree to their canonical form."""

    # Validate arguments
    if not isinstance(input_path, Path):
        raise ValueError(f'Input path is not a Path object.')
    if not isinstance(output_path, Path):
        raise ValueError(f'Output path is not a Path object.')

    # Load the main tree that support values will be added to
    log.info(f'Loading input tree: {input_path}')
    tree = dendropy.Tree.get_from_path(
        str(input_path),
        schema='newick',
        preserve_underscores=True
    )

    # Update the labels for each taxon
    labels_seen = dict()
    for taxon in track(tree.taxon_namespace, description='Processing...'):
        gid = canonical_gid(taxon.label)
        if gid in labels_seen:
            log.warning(f'Leaf node {taxon.label} -> {gid} is a duplicate of {labels_seen[gid]}')
        taxon.label = gid
        labels_seen[gid] = taxon.label

    # Save the tree
    tree.write_to_path(str(output_path), schema='newick', suppress_rooting=True, unquoted_underscores=True)
    log.info(f'Wrote tree to: {output_path}')
