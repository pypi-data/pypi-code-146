from pathlib import Path
from typing import Union

from lnschema_core.dev import id


def generate_cell_ranger_files(sample_name: str, basedir: Union[str, Path]):
    """Generate mock cell ranger outputs.

    Args:
        sample_name: name of the sample
        basedir: run directory

    """
    basedir = Path(basedir)

    fastqdir = basedir / "fastq"
    fastqdir.mkdir(parents=True, exist_ok=True)
    fastqfile1 = fastqdir / f"{sample_name}_R1_001.fastq.gz"
    fastqfile1.touch(exist_ok=True)
    fastqfile2 = fastqdir / f"{sample_name}_R2_001.fastq.gz"
    fastqfile2.touch(exist_ok=True)

    sampledir = basedir / f"{sample_name}"
    for folder in ["raw_feature_bc_matrix", "filtered_feature_bc_matrix", "analysis"]:
        filedir = sampledir / folder
        filedir.mkdir(parents=True, exist_ok=True)

    for filename in [
        "web_summary.html",
        "metrics_summary.csv",
        "possorted_genome_bam.bam",
        "possorted_genome_bam.bam.bai",
        "molecule_info.h5",
        "cloupe.cloupe",
        "raw_feature_bc_matrix.h5",
        "raw_feature_bc_matrix/barcodes.tsv.gz",
        "raw_feature_bc_matrix/features.tsv.gz",
        "raw_feature_bc_matrix/matrix.mtx.gz",
        "filtered_feature_bc_matrix.h5",
        "filtered_feature_bc_matrix/barcodes.tsv.gz",
        "filtered_feature_bc_matrix/features.tsv.gz",
        "filtered_feature_bc_matrix/matrix.mtx.gz",
        "analysis/analysis.csv",
    ]:
        filedir = sampledir / filename
        filedir.touch(exist_ok=True)

    for filepath in basedir.rglob("*"):
        if not filepath.is_dir():
            with open(filepath, "w") as file:
                file.write(f"{id.base62(n_char=6)}")
