import pandas as pd
import gzip

from logging import Logger

# Take the caris RNA information from the provided tsv for ingestion and input to TSO/pcann
# We are not guaranteed rnaseq results FYI
def convert_tsv_to_rgel(prefix, files, ingest_status, log: Logger):
    if ingest_status["run_instructions"]["som_rna"]:
        tsv_file = files["tsv"]
        log.info(f"RNA TPM file found. Converting to RGEL: {tsv_file}")
        df = pd.read_table(tsv_file, comment="#", header=None)
        df.rename(columns={0: "gene_id", 1: "expression"}, inplace=True)

        df["sample_id"] = prefix
        df["gene_name"] = df["gene_id"]
        df["raw_count"] = ""
        df["attributes"] = "{}"
        df["is_normalized"] = "True"
        df["expression_unit"] = "tpm"

        df.drop_duplicates(inplace=True)
        # Select columns for output
        df_out = df[
            [
                "sample_id",
                "gene_id",
                "gene_name",
                "expression",
                "raw_count",
                "attributes",
                "is_normalized",
                "expression_unit",
            ]
        ]

        df_out.to_csv(f"{prefix}.expression.rgel.gz", compression="gzip", na_rep="", index=False)
        return {
            "fileName": f".lifeomic/caris/{prefix}/{prefix}.expression.rgel.gz",
            "sequenceType": "somatic",
            "type": "expression",
        }
    # Empty RGEL with just a header, don't want it in the manifest file because duh, it's empty. It gets passed on to TSOI prediction.
    with gzip.open(f"{prefix}.expression.rgel.gz", "w") as f:
        f.write(
            b"sample_id,gene_id,gene_name,expression,raw_count,attributes,is_normalized,expression_unit\n"
        )

    return None
