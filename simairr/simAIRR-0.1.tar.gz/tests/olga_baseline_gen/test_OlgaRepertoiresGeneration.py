from simAIRR.olga_baseline_gen.OlgaRepertoiresGeneration import OlgaRepertoiresGeneration
import os


def test_olga_repertoires_generation(tmp_path):
    olga_reps = OlgaRepertoiresGeneration(model='humanTRB', output_file_path=tmp_path,
                                          n_seq=9, seed=1234,
                                          n_reps=10, n_threads=2)
    olga_reps.olga_generate_multiple_repertoires()
    files = [fn for fn in os.listdir(tmp_path) if os.path.isfile(os.path.join(tmp_path, fn))]
    print(tmp_path)
    assert len(files) == 10
    num_lines = sum(1 for line in open(os.path.join(tmp_path, 'rep_9.tsv')))
    assert num_lines == 9