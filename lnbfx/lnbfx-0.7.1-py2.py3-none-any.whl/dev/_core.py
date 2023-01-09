from pathlib import Path
from typing import Union

BFX_FILE_TYPES = {
    "abi": "abi",
    "aln": "aln",
    "bai": "bai",
    "bam": "bam",
    "bcf": "bcf",
    "bed": "bed",
    "blc": "blc",
    "bw": "bigwig",
    "bigwig": "bigwig",
    "cram": "cram",
    "embl": "embl",
    "fa": "fasta",
    "faa": "fasta",
    "fas": "fasta",
    "fasta": "fasta",
    "ffn": "fasta",
    "fna": "fasta",
    "frn": "fasta",
    "fastq": "fastq",
    "fq": "fastq",
    "gb": "genbank",
    "gbk": "genbank",
    "genbank": "genbank",
    "gff": "gff",
    "gtf": "gtf",
    "mdl": "mdl",
    "msf": "msf",
    "pdb": "pdb",
    "pir": "pir",
    "pfam": "pfam",
    "phy": "phy",
    "sam": "sam",
    "sff": "sff",
    "stk": "stk",
    "sto": "sto",
    "vcf": "vcf",
    "wig": "wig",
}


def annotate_bfx_file_type(path: Union[Path, str]) -> Union[str, None]:
    if isinstance(path, str):
        path = Path(path)
    suffix = path.suffix[1:].lower()
    if suffix in ["gz", "tar", "zip"]:
        suffix = path.stem.split(".")[-1]
    if suffix in BFX_FILE_TYPES.keys():
        return BFX_FILE_TYPES[suffix]
    elif any(substr in path.name for substr in ["_fastqc.html", "_fastqc.zip"]):  # noqa
        return "fastqc"
    else:
        return None
