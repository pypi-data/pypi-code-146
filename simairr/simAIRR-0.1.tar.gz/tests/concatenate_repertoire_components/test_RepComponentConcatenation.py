from simAIRR.concatenate_repertoire_components.RepComponentConcatenation import RepComponentConcatenation
import os
import pandas as pd
import numpy as np


def test_public_private_multi_concatenate_repertoire_components(tmp_path):
    super_path = tmp_path / "baseline_repertoires"
    primary_reps_path = super_path / "corrected_public_repertoires"
    secondary_reps_path = super_path / "filtered_private_repertoires"
    concatenated_reps_path = tmp_path / "corrected_baseline_repertoires"
    super_path.mkdir()
    primary_reps_path.mkdir()
    secondary_reps_path.mkdir()
    df = pd.DataFrame(np.random.randint(0, 100, size=(100, 5)), columns=list('ABCDE'))
    for idx, chunk in enumerate(np.array_split(df, 10)):
        chunk.to_csv(primary_reps_path / f'rep_{idx}.tsv', index=None, header=None, sep='\t')
        chunk.to_csv(secondary_reps_path / f'rep_{idx}.tsv', index=None, header=None, sep='\t')
    rep_concat = RepComponentConcatenation(components_type = "public_private", super_path=super_path, n_threads=2)
    rep_concat.multi_concatenate_repertoire_components()
    concatenated_files = [fn for fn in os.listdir(concatenated_reps_path) if os.path.isfile(os.path.join(concatenated_reps_path, fn))]
    assert len(concatenated_files) == 10
    try:
        rep_1 = pd.read_csv(os.path.join(concatenated_reps_path, "rep_1.tsv"), header=None, index_col=None, sep='\t')
        assert rep_1.shape[0] == 20
    except (pd.errors.EmptyDataError, FileNotFoundError) as e:
        print(e)
