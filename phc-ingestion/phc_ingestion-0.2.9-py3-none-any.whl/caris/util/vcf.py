import datetime
import gzip
import io
import os
import re
import subprocess
import sys
import zipfile

from logging import Logger
from pysam import tabix_compress


# This is done in next step, we are just adding to yaml
def extract_sv(prefix, ingest_status):
    vcfs = []

    if ingest_status["run_instructions"]["som_vcf"]:
        vcfs.append(
            {
                "fileName": f".lifeomic/caris/{prefix}/{prefix}.lifted.modified.somatic.nrm.filtered.vcf.gz",
                "sequenceType": "somatic",
                "type": "shortVariant",
            }
        )
    else:
        # Create a VCF file with an empty header if none was provided
        fout = gzip.open(f"{prefix}.somatic.vcf.gz", "w")
        # Check it out it's the VCF header ONLY
        foutW = io.TextIOWrapper(fout, encoding="utf-8")
        foutW.write("##fileformat=VCFv4.1\n")
        foutW.write("##filedate=" + datetime.datetime.now().isoformat() + "\n")
        foutW.write('##FILTER=<ID=PASS,Description="All filters passed">\n')
        foutW.write('##FILTER=<ID=R8,Description="IndelRepeatLength is greater than 8">\n')
        foutW.write(
            '##FILTER=<ID=R8.1,Description="IndelRepeatLength of a monomer is greater than 8">\n'
        )
        foutW.write(
            '##FILTER=<ID=R8.2,Description="IndelRepeatLength of a dimer is greater than 8">\n'
        )
        foutW.write('##FILTER=<ID=sb,Description="Variant strand bias high">\n')
        foutW.write(
            '##FILTER=<ID=sb.s,Description="Variant strand bias significantly high (only for SNV)">\n'
        )
        foutW.write(
            '##FILTER=<ID=rs,Description="Variant with rs (dbSNP) number in a non-core gene">\n'
        )
        foutW.write(
            '##FILTER=<ID=FP,Description="Possibly false positives due to high similarity to off-target regions">\n'
        )
        foutW.write('##FILTER=<ID=NC,Description="Noncoding INDELs on non-core genes">\n')
        foutW.write('##FILTER=<ID=lowDP,Description="low depth variant">\n')
        foutW.write('##FILTER=<ID=Benign,Description="Benign variant">\n')
        foutW.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
        foutW.write(
            '##FORMAT=<ID=AF,Number=1,Type=String,Description="Variant Allele Frequency">\n'
        )
        foutW.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t" + prefix + "\n")

        foutW.close()

    if ingest_status["run_instructions"]["germ_vcf"]:
        vcfs.append(
            {
                "fileName": f".lifeomic/caris/{prefix}/{prefix}.lifted.modified.germline.nrm.filtered.vcf.gz",
                "sequenceType": "germline",
                "type": "shortVariant",
            }
        )
    else:
        # Create a VCF file with an empty header if none was provided
        fout = gzip.open(f"{prefix}.germline.vcf.gz", "w")
        # Check it out it's the VCF header ONLY
        foutW = io.TextIOWrapper(fout, encoding="utf-8")
        foutW.write("##fileformat=VCFv4.1\n")
        foutW.write("##filedate=" + datetime.datetime.now().isoformat() + "\n")
        foutW.write('##FILTER=<ID=PASS,Description="All filters passed">\n')
        foutW.write('##FILTER=<ID=R8,Description="IndelRepeatLength is greater than 8">\n')
        foutW.write(
            '##FILTER=<ID=R8.1,Description="IndelRepeatLength of a monomer is greater than 8">\n'
        )
        foutW.write(
            '##FILTER=<ID=R8.2,Description="IndelRepeatLength of a dimer is greater than 8">\n'
        )
        foutW.write('##FILTER=<ID=sb,Description="Variant strand bias high">\n')
        foutW.write(
            '##FILTER=<ID=sb.s,Description="Variant strand bias significantly high (only for SNV)">\n'
        )
        foutW.write(
            '##FILTER=<ID=rs,Description="Variant with rs (dbSNP) number in a non-core gene">\n'
        )
        foutW.write(
            '##FILTER=<ID=FP,Description="Possibly false positives due to high similarity to off-target regions">\n'
        )
        foutW.write('##FILTER=<ID=NC,Description="Noncoding INDELs on non-core genes">\n')
        foutW.write('##FILTER=<ID=lowDP,Description="low depth variant">\n')
        foutW.write('##FILTER=<ID=Benign,Description="Benign variant">\n')
        foutW.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
        foutW.write(
            '##FORMAT=<ID=AF,Number=1,Type=String,Description="Variant Allele Frequency">\n'
        )
        foutW.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t" + prefix + "\n")

        foutW.close()

    # We do not want this empty file in the manifest.
    return vcfs


def process_caris_vcf(infile, outpath, file_name, log: Logger):

    if "germline.vcf" in infile:
        out_vcf = f"{outpath}/{file_name}.modified.germline.vcf"
    else:
        out_vcf = f"{outpath}/{file_name}.modified.somatic.vcf"

    if infile.endswith(".gz"):
        fin = gzip.open(infile, "rb")
    else:
        if zipfile.is_zipfile(infile):
            zfile = zipfile.ZipFile(infile)
            if len(zfile.namelist()) > 1:
                log.exception(
                    "ERROR: sample {} file {} is a zipped multiple files archive.".format(
                        file_name, infile
                    )
                )
                sys.exit(9)
            fin = subprocess.Popen("unzip -p " + infile, shell=True, stdout=subprocess.PIPE).stdout
        else:
            fin = open(infile, "rb")

    fout = open(out_vcf, "wb+")

    foutW = io.TextIOWrapper(fout, encoding="utf-8")
    foutW.write("##fileformat=VCFv4.1\n")
    foutW.write("##filedate=" + datetime.datetime.now().isoformat() + "\n")
    foutW.write('##FILTER=<ID=PASS,Description="All filters passed">\n')
    foutW.write('##FILTER=<ID=R8,Description="IndelRepeatLength is greater than 8">\n')
    foutW.write(
        '##FILTER=<ID=R8.1,Description="IndelRepeatLength of a monomer is greater than 8">\n'
    )
    foutW.write('##FILTER=<ID=R8.2,Description="IndelRepeatLength of a dimer is greater than 8">\n')
    foutW.write('##FILTER=<ID=sb,Description="Variant strand bias high">\n')
    foutW.write(
        '##FILTER=<ID=sb.s,Description="Variant strand bias significantly high (only for SNV)">\n'
    )
    foutW.write(
        '##FILTER=<ID=rs,Description="Variant with rs (dbSNP) number in a non-core gene">\n'
    )
    foutW.write(
        '##FILTER=<ID=FP,Description="Possibly false positives due to high similarity to off-target regions">\n'
    )
    foutW.write('##FILTER=<ID=NC,Description="Noncoding INDELs on non-core genes">\n')
    foutW.write('##FILTER=<ID=lowDP,Description="low depth variant">\n')
    foutW.write('##FILTER=<ID=Benign,Description="Benign variant">\n')
    foutW.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
    foutW.write(
        '##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths for the ref and alt alleles in the order listed">\n'
    )
    foutW.write('##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read depth">\n')
    foutW.write('##INFO=<ID=AF,Number=1,Type=String,Description="Variant Allele Frequency">\n')

    if "germline" in infile:
        sample_name = "germline_" + file_name
    else:
        sample_name = file_name

    foutW.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t" + sample_name + "\n")

    finR = io.BufferedReader(fin)

    for bline in finR:
        record = re.sub(" ", "", bline.decode("utf-8").rstrip("\r\n"))
        if len(record) == 0 or record.startswith("#"):
            continue
        recList = record.split("\t")
        if len(recList) < 4 or not recList[1].isdigit():
            log.exception(
                "ERROR: genomic record has missing or invalid fields: [{}]".format(
                    "\t".join(recList)
                )
            )
            sys.exit(11)

        # Stuff we don't want to change
        genomic_record = "\t".join(recList[0:7])
        info_field_list = recList[7].split(";")

        vcf_format = "GT:AD:DP"

        sample_field_list = recList[9].split(":")

        depth = "0"
        for data in info_field_list:
            if data.split("=")[0] == "DP":
                depth = data.split("=")[1]

        # We need to put this in the proper format for ingestion into omics explore.
        new_sample_field = ":".join([sample_field_list[0], sample_field_list[2], depth])

        vcf_info = f"AF={sample_field_list[1]}"

        foutW.write("\t".join([genomic_record, vcf_info, vcf_format, new_sample_field]) + "\n")

    finR.close()
    foutW.close()

    tabix_compress(out_vcf, f"{out_vcf}.gz", force=True)
    os.remove(out_vcf)
