import glob
import gzip
import json
import os
import pysam
import shutil

from ingestion.caris.util.tar import unpack
from ingestion.caris.util.metadata import extract_metadata
from ingestion.caris.util.structural import extract_structural
from ingestion.caris.util.cnv import extract_cnv
from ingestion.caris.util.tsv import convert_tsv_to_rgel
from ingestion.caris.util.vcf import extract_sv
from ingestion.caris.util.ga4gh import create_yaml
from logging import Logger

CARIS_CASE_ID_LENGTH = len("TN22-000000")


def process_caris_json(
    infile: str, outpath: str, file_name: str, source_file_id: str, ingest_status: dict, log: Logger
):

    # Unpack tarball and go into the new directory
    unpack(infile, outpath)
    os.chdir(outpath)
    # If we do this we need to make sure we communicate it well.
    #  shutil.move(args.input, f'{outpath}/{os.path.basename(args.input)}')
    file_list = glob.glob("*")
    files = {}

    files["bam"] = []
    files["R1.fastq.gz"] = []
    files["R2.fastq.gz"] = []

    for file in file_list:
        extension = file.split(".")[1:]
        if not isinstance(extension, str):
            extension = ".".join(extension)
        # We can have multiple bam files (RNA and DNA)
        if extension == "bam" or "fastq" in extension:
            files[extension].append(file)
        elif file.lower().startswith("germline"):
            files["germline.vcf"] = file
        elif file.endswith("vcf") and "germline" not in file:
            files["somatic.vcf"] = file
        else:
            files[extension] = file

    log.info(f"Files in tarball input: {file_list}")

    json_file = files["json"]

    f = open(json_file, "rb")
    all_data = json.load(f)
    data = all_data
    if "root" in all_data.keys():
        data = all_data["root"]
    f.close()

    somatic_filename = None
    germline_filename = None
    germline_case_id = None

    # Sometimes they don't come in gzipped
    for key in files.keys():
        if "somatic.vcf" in key:
            somatic_filename = files["somatic.vcf"].replace(".vcf", ".somatic.vcf") + ".gz"
            with open(files["somatic.vcf"], "rb") as f_in:
                with gzip.open(somatic_filename, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            ingest_status["run_instructions"]["som_vcf"] = True
        if "germline.vcf" in key:
            germline_filename = (
                files["germline.vcf"].replace("Germline_", "").replace(".vcf", ".germline.vcf")
                + ".gz"
            )
            with open(files["germline.vcf"], "rb") as f_in:
                with gzip.open(germline_filename, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            ingest_status["run_instructions"]["germ_vcf"] = True
            germline_case_id = files["germline.vcf"].replace("Germline_", "")[
                0:CARIS_CASE_ID_LENGTH
            ]
    if "tsv" in files.keys():
        ingest_status["run_instructions"]["som_rna"] = True

    # Get patient
    metadata = extract_metadata(data, file_name, files, source_file_id, ingest_status, log)
    structural_results = extract_structural(file_name, data, ingest_status, log)
    cnv_results = extract_cnv(file_name, data, ingest_status)
    rgel_results = convert_tsv_to_rgel(file_name, files, ingest_status, log)
    vcf_results = extract_sv(file_name, ingest_status)

    # We might not have any of these files but we need an empty json object here.
    metadata["files"] = []
    if structural_results:
        metadata["files"].append(structural_results)
    if rgel_results:
        metadata["files"].append(rgel_results)
    if cnv_results:
        metadata["files"].append(cnv_results)
    if vcf_results:
        metadata["files"] = metadata["files"] + vcf_results

    # Get bam indexing out of the way ;P they're big files typically. This adds a lot of time to the run because bam files are HUGE.
    if "bam" in files.keys() and files["bam"]:
        log.info(f"indexing bam file(s): {files['bam']}")
        # We could have DNA and RNA bam.
        for filename in files["bam"]:
            pysam.index(filename)

    create_yaml(metadata, file_name, ingest_status)

    # Return VCF files for immediate processing
    result = {}

    if somatic_filename is not None:
        result["somatic_vcf"] = f"{outpath}/{somatic_filename}"
    if germline_filename is not None:
        result["germline_vcf"] = f"{outpath}/{germline_filename}"

    return (result, germline_case_id)
