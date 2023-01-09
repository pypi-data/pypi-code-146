from pathlib import Path

from lnbfx.dev import annotate_bfx_file_type


def test_annotate_bfx_file_type():
    file_types = {
        "sample.bam": "bam",
        "sample.bam.gz": "bam",
        "sample.bam.bai": "bai",
        "sample.sam": "sam",
        "sample.fastq": "fastq",
        "sample.bcf": "bcf",
        "sample.vcf": "vcf",
        "sample_fastqc.html": "fastqc",
        "sample": None,
    }
    for k, v in file_types.items():
        assert annotate_bfx_file_type(Path(k)) == v
