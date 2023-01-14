import os

from ingestion.caris.util.json import process_caris_json
from ingestion.caris.util.vcf import process_caris_vcf
from lifeomic_logging import scoped_logger


INGEST_STATUS = {
    "exome_performed": False,
    "cnv_performed": False,
    "ihc_performed": False,
    "structural_performed": False,
    "run_instructions": {
        "som_vcf": False,
        "germ_vcf": False,
        "som_rna": False,
        "som_structural": False,
        "som_cnv": False,
    },
}


def process_caris(infile, outpath, file_name, source_file_id):
    with scoped_logger(__name__) as log:
        os.makedirs(f"{outpath}", exist_ok=True)
        result, germline_case_id = process_caris_json(
            infile, outpath, file_name, source_file_id, INGEST_STATUS, log
        )
        if "somatic_vcf" in result:
            process_caris_vcf(result["somatic_vcf"], outpath, file_name, log)
        if "germline_vcf" in result:
            process_caris_vcf(result["germline_vcf"], outpath, file_name, log)
        return germline_case_id
