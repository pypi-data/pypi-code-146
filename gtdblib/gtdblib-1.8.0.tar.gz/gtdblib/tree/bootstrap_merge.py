import multiprocessing as mp
from math import floor
from pathlib import Path
from typing import Collection

import dendropy
import numpy as np
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

from gtdblib import log


def bootstrap_merge_replicates(
        input_tree: Path,
        output_tree: Path,
        replicate_trees: Collection[Path],
        cpus: int = 1
):
    """Calculates non-parametric bootstraps for monophyletic groups and
    transposes them to the input tree.

    :param input_tree: The tree to merge the bootstraps to.
    :param output_tree: The path to write the tree to.
    :param replicate_trees: The trees to calculate the bootstraps from.
    :param cpus: The number of processes to use.
    """

    # Validate arguments
    if not isinstance(input_tree, Path):
        raise ValueError(f'Input tree is not a Path object.')
    if not isinstance(output_tree, Path):
        raise ValueError(f'Output tree is not a Path object.')
    if not isinstance(replicate_trees, Collection):
        raise ValueError(f'Replicate trees is not a Collection object.')
    if not all(isinstance(x, Path) for x in replicate_trees):
        raise ValueError(f'Not all replicate trees are Path objects.')
    if cpus is None or not isinstance(cpus, int) or cpus < 1:
        cpus = 1

    # Load the main tree that support values will be added to
    tree = dendropy.Tree.get_from_path(
        str(input_tree),
        schema='newick',
        rooting='force-unrooted',
        preserve_underscores=True
    )

    # Seed the support values
    for node in tree.internal_nodes():
        node.label = 0
        node.nontrivial_splits = 0

    # Store a consistent ordering of the internal nodes
    input_internal_nodes = tuple(tree.internal_nodes(), )

    # Generate the descendant taxa for those nodes
    input_desc_taxa = tuple([frozenset({y.taxon.label for y in x.leaf_nodes()}) for x in input_internal_nodes])

    # Process the input descendant taxa and
    results = list()
    with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            refresh_per_second=1
    ) as p_bar:
        task_total = p_bar.add_task(
            total=100,
            description=f'Processing tree 1 of {len(replicate_trees):,}'
        )

        # Process each of the trees
        for rep_tree_path in replicate_trees:
            results.append(_calculate_support_worker(
                rep_tree_path,
                input_desc_taxa,
                p_bar,
                task_total,
                len(replicate_trees),
                cpus
            ))
            p_bar.update(
                task_total,
                description=f'Processing tree {len(results):,} of {len(replicate_trees):,}'
            )

    # Append the split information to the nodes
    for result in results:
        for node, (n_support, n_non_trivial_split) in zip(input_internal_nodes, result):
            node.label += n_support
            node.nontrivial_splits += n_non_trivial_split

    # Calculate the %
    for node in tree.internal_nodes():
        if node.nontrivial_splits > 0:
            node.label = str(int(floor(node.label * 100.0 / node.nontrivial_splits)))
        else:
            node.label = 'NA'

    tree.write_to_path(str(output_tree), schema='newick', suppress_rooting=True, unquoted_underscores=True)
    log.info(f'Wrote tree to: {output_tree}')

    return


def _calculate_split_worker(jobs):
    idx, cur_taxa_labels, rep_tree_taxa_set, d_taxon_label_to_bit_idx, all_taxa_bitmask, rep_tree_list = jobs

    # Only calculate the support for splits that are present in the reference tree
    common_taxon_labels = cur_taxa_labels.intersection(rep_tree_taxa_set)

    # Store the number of supported splits
    if len(common_taxon_labels) > 1:

        # Create the bit vector for the taxa
        # This works as the bit shift done (1 << i) will always produce a
        # bit vector with only one significant bit (i.e. the index of the
        # taxon in the taxon namespace)
        split_bit_vec = np.zeros(len(rep_tree_taxa_set), dtype=np.bool)
        split_bit_vec[[d_taxon_label_to_bit_idx[x] for x in common_taxon_labels]] = True

        # Reverse the ordering (as idx=0 should be 001, not 100)
        split_bit_str = ''.join(['1' if x else '0' for x in reversed(split_bit_vec)])

        # Calculate the split support
        split = int(split_bit_str, 2)
        normalized_split = dendropy.Bipartition.normalize_bitmask(
            bitmask=split,
            fill_bitmask=all_taxa_bitmask,
            lowest_relevant_bit=1)

        n_support = int(rep_tree_list.frequency_of_bipartition(split_bitmask=normalized_split))
        n_non_trivial_split = 1
    else:
        n_support = 0
        n_non_trivial_split = 0

    # Save the result
    return idx, n_support, n_non_trivial_split


def _calculate_support_worker(rep_tree_path, taxa_labels, p_bar, task_total, n_trees, cpus):
    """Worker to calculate the support for splits."""

    # Load the tree
    rep_tree = dendropy.Tree.get_from_path(
        str(rep_tree_path),
        schema='newick',
        rooting='force-unrooted',
        preserve_underscores=True
    )
    all_taxa_bitmask = rep_tree.taxon_namespace.all_taxa_bitmask()

    # Calculate the descendant taxa for the reference tree
    rep_tree_list = dendropy.TreeList([rep_tree])
    rep_tree_taxa_set = frozenset({x.taxon.label for x in rep_tree.leaf_node_iter()})

    # Get the bitmask for all taxa that are common
    d_taxon_label_to_bit_idx = {x.label: i for i, x in enumerate(rep_tree.taxon_namespace)}

    # Iterate over the reference tree taxa internal nodes (order is consistent)
    jobs = list()
    for idx, cur_taxa_labels in enumerate(taxa_labels):
        jobs.append((
            idx,
            cur_taxa_labels,
            rep_tree_taxa_set,
            d_taxon_label_to_bit_idx,
            all_taxa_bitmask,
            rep_tree_list
        ))

    # Create a progress bar and process the jobs
    task_inner = p_bar.add_task(f"{rep_tree_path.name}", total=len(jobs))
    d_idx_to_result = dict()
    pct_per_job = 100 / len(jobs) / n_trees

    # Process the jobs single-threaded
    if cpus == 1:
        for result in (_calculate_split_worker(job) for job in jobs):
            d_idx_to_result[result[0]] = result[1:]
            p_bar.update(task_inner, advance=1)
            p_bar.update(task_total, advance=pct_per_job)

    # Process multiple jobs in parallel
    with mp.Pool(processes=cpus) as pool:
        for result in pool.imap_unordered(_calculate_split_worker, jobs, chunksize=10):
            d_idx_to_result[result[0]] = result[1:]
            p_bar.update(task_inner, advance=1)
            p_bar.update(task_total, advance=pct_per_job)

    # Remove the progress bar for this tree
    p_bar.remove_task(task_inner)

    # Return the results (in the same order)
    results = [d_idx_to_result[i] for i in range(len(taxa_labels))]
    return tuple(results, )
