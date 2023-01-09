"""Small example datasets.

.. autosummary::
   :toctree: .

   file_fastq
   scrnaseq_cellranger

"""

from pathlib import Path
from urllib.request import urlretrieve


def file_fastq() -> Path:
    """Return fastq file example."""
    filepath, _ = urlretrieve(
        "https://lamindb-test.s3.amazonaws.com/SRR4238351_subsamp.fastq.gz",
        "SRR4238351_subsamp.fastq.gz",
    )
    return Path(filepath)


def scrnaseq_cellranger() -> Path:
    """Directory with exemplary scrnaseq cellranger output."""
    filepath, _ = urlretrieve(
        "https://lamindb-test.s3.amazonaws.com/scrnaseq-cellranger.zip",
    )
    from zipfile import ZipFile

    with ZipFile(filepath, "r") as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall(path=".")

    return Path("scrnaseq-cellranger")
