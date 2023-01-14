import os
from shutil import copyfile
from typing import Union


def is_number(s: str):
    try:
        float(s)
        return True
    except ValueError:
        return False


# if date_field is a string then return it as the date
# otherwise, it's a dictionary (due to namespace) so return the `#text` field
def get_date(date_field: Union[str, dict]):
    if isinstance(date_field, str):
        return date_field
    return date_field.get("#text")


def get_mrn(pmi) -> str:
    return pmi["MRN"] if pmi.get("MRN") else ""


def get_trf(sample) -> str:
    return sample.get("TRFNumber", "")


def get_med_facil(pmi) -> list:
    med_facil_info = []
    med_facil_info.append(pmi.get("MedFacilName", ""))
    med_facil_info.append(pmi.get("MedFacilID", ""))
    return med_facil_info


def get_ordering_md(pmi, npi) -> list:
    ordering_md_info = []
    ordering_md_info.append(pmi.get("OrderingMD", ""))
    ordering_md_info.append(npi)
    return ordering_md_info


def get_non_human_content(nhc_dicts) -> list:
    nhc_final = []

    if isinstance(nhc_dicts, list):
        for sub_dict in nhc_dicts:
            nhc_final.append(
                {
                    "nhcOrganism": sub_dict.get("@organism", "unknown"),
                    "nhcReadsPerMil": float(sub_dict.get("@reads-per-million", 0.0)),
                    "nhcStatus": sub_dict.get("@status", "unknown"),
                }
            )

    else:
        nhc_final.append(
            {
                "nhcOrganism": nhc_dicts.get("@organism", "unknown"),
                "nhcReadsPerMil": float(nhc_dicts.get("@reads-per-million", 0.0)),
                "nhcStatus": nhc_dicts.get("@status", "unknown"),
            }
        )

    return nhc_final


def get_plasma_tumor_fraction(genes) -> str:
    ptf_dict = {
        "Elevated Tumor Fraction": "Elevated",
        "Elevated Tumor Fraction Not Detected": "Not Elevated",
        "Cannot Be Determined": "Undetermined",
    }
    ptf_entry = [
        entry for entry in genes.get("Gene", {}) if entry.get("Name", "") == "Tumor Fraction"
    ]
    if ptf_entry:
        ptf_val = ptf_entry[0].get("Alterations", "").get("Alteration", "").get("Name", "")
        return [value for (key, value) in ptf_dict.items() if key == ptf_val][0]
    else:
        return None


def get_test_yml(
    customer_info_dict: dict,
    results_payload_dict: dict,
    base_xml_name: str,
    local_output_dir: str,
    report_file: str,
    write_vcf_to_manifest: bool,
    phc_output_dir: str,
    source_file_id: str,
) -> dict:
    npi = customer_info_dict.get("rr:NPI", "")
    pmi = results_payload_dict.get("FinalReport", {}).get("PMI", {})
    signatures = results_payload_dict.get("FinalReport", {}).get("Signatures")
    sample = results_payload_dict.get("FinalReport", {}).get("Sample", {})
    variant_report = results_payload_dict.get("variant-report", {})
    biomarkers = variant_report.get("biomarkers", {})
    non_human_content = variant_report.get("non-human-content", {})
    report_properties = results_payload_dict.get("FinalReport", {}).get("reportProperties", {})
    report_property = report_properties.get("reportProperty", [])
    genes = results_payload_dict.get("FinalReport", {}).get("Genes", {})
    plasma_tumor_fraction = get_plasma_tumor_fraction(genes)
    properties = report_property if isinstance(report_property, list) else [report_property]
    gw_loh = next(
        (prop for prop in properties if prop.get("@key") == "LossOfHeterozygosityScore"),
        None,
    )

    os.makedirs(f"{local_output_dir}/{base_xml_name}", exist_ok=True)

    mrn = get_mrn(pmi)

    trf = get_trf(sample)

    med_facil_info = get_med_facil(pmi)

    ordering_md_info = get_ordering_md(pmi, npi)

    # fallback on previous behavior for indexedDate if value is not found
    indexedDate = get_date(pmi.get("CollDate")) or get_date(sample.get("ReceivedDate"))

    # store both values sperately
    receivedDate = get_date(sample.get("ReceivedDate"))
    collDate = get_date(pmi.get("CollDate"))

    # store date of published report
    reportDate = str(get_date(signatures.get("Signature").get("ServerTime")))[0:10]

    yaml_file = {
        "name": "Foundation Medicine",
        "reference": "GRCh37",
        "sourceFileId": source_file_id,
        "testType": sample.get("TestType"),
        "indexedDate": indexedDate,
        "receivedDate": receivedDate,
        "collDate": collDate,
        "reportDate": reportDate,
        "reportID": trf,
        "mrn": mrn,
        "patientDOB": get_date(pmi.get("DOB")),
        "patientLastName": pmi.get("LastName"),
        "medFacilName": med_facil_info[0],
        "medFacilID": med_facil_info[1],
        "orderingMDName": ordering_md_info[0],
        "orderingMDNPI": ordering_md_info[1],
        "bodySite": variant_report.get("@tissue-of-origin"),
        "bodySiteSystem": "http://lifeomic.com/fhir/sequence-body-site",
        "bodySiteDisplay": variant_report.get("@tissue-of-origin"),
        "indication": pmi.get("SubmittedDiagnosis"),
        "indicationDisplay": pmi.get("SubmittedDiagnosis"),
        "indicationSystem": "http://lifeomic.com/fhir/sequence-indication",
        "files": [
            {
                "type": "copyNumberVariant",
                "sequenceType": "somatic",
                "fileName": f"{phc_output_dir}/{base_xml_name}/{base_xml_name}.copynumber.csv",
            },
            {
                "type": "structuralVariant",
                "sequenceType": "somatic",
                "fileName": f"{phc_output_dir}/{base_xml_name}/{base_xml_name}.structural.csv",
            },
        ],
    }

    if write_vcf_to_manifest:
        yaml_file["files"].append(
            {
                "type": "shortVariant",
                "sequenceType": "somatic",
                "fileName": f"{phc_output_dir}/{base_xml_name}/{base_xml_name}.nrm.vcf.gz",
            }
        )

    yaml_file["patientInfo"] = {
        "firstName": pmi.get("FirstName"),
        "lastName": pmi.get("LastName"),
        "gender": pmi.get("Gender").lower(),
        "dob": get_date(pmi.get("DOB")),
    }

    if mrn:
        yaml_file["patientInfo"]["identifiers"] = [
            {
                "codingSystem": "http://hl7.org/fhir/v2/0203",
                "codingCode": "MR",
                "value": pmi.get("MRN"),
            }
        ]

    if gw_loh:
        values = {"loh-high": "high", "loh-low": "low"}
        alterations = []
        gene = genes.get("Gene", [])
        genes_list = gene if isinstance(gene, list) else [gene]
        for gene in genes_list:
            alt = gene.get("Alterations", {}).get("Alteration", [])
            alterations.extend(alt) if isinstance(alt, list) else alterations.append(alt)

        loh_alt: dict = next(
            (alt for alt in alterations if values.get(alt.get("Name", "").lower())), {}
        )

        value = gw_loh.get("value", "").replace("%", "")
        # it is possible that value is "Units Not Reported"
        yaml_file["lossOfHeterozygosityScore"] = float(value) if is_number(value) else -1
        yaml_file["lossOfHeterozygosityStatus"] = values.get(
            loh_alt.get("Name", "").lower(), "unknown"
        )

    if biomarkers and "microsatellite-instability" in biomarkers:
        values = {
            "MSI-H": "high",
            "MSI-L": "low",
            "MSS": "stable",
            "unknown": "indeterminate",
        }
        microsatellite_dict = biomarkers["microsatellite-instability"]
        yaml_file["msi"] = values.get(microsatellite_dict.get("@status", "unknown"))

    if biomarkers and "tumor-mutation-burden" in biomarkers:
        tumor_dict = biomarkers["tumor-mutation-burden"]
        yaml_file["tmb"] = tumor_dict.get("@status", "unknown")
        yaml_file["tmbScore"] = float(tumor_dict.get("@score"))

    # adding non-human content fields
    if non_human_content != None:
        yaml_file["nonHumanContent"] = get_non_human_content(non_human_content.get("non-human", ""))

    if report_file:
        copyfile(report_file, f"{local_output_dir}/{base_xml_name}/{base_xml_name}.report.pdf")

        yaml_file["reportFile"] = f"{phc_output_dir}/{base_xml_name}/{base_xml_name}.report.pdf"

    # add plasma tumor fraction
    if plasma_tumor_fraction:
        yaml_file["plasmaTumorFraction"] = plasma_tumor_fraction

    return yaml_file
