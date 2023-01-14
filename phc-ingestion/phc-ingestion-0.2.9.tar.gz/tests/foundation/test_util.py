import gzip
import csv
import os
import shutil
import xmltodict

from ingestion.foundation.util.cnv import extract_copy_numbers
from ingestion.foundation.util.fnv import extract_fusion_variant
from ingestion.foundation.util.ga4gh import (
    get_med_facil,
    get_ordering_md,
    get_test_yml,
    get_mrn,
    get_trf,
    get_non_human_content,
    get_plasma_tumor_fraction,
)
from ingestion.foundation.util.vcf_etl import vcf_etl, transform_scientific_notation_in_af

BASE_PATH = os.path.abspath(os.path.dirname(__file__))


class MockLog:
    def info(self, _: str):
        pass


def read_xml(xml_file):
    with open(xml_file) as fd:
        return xmltodict.parse(fd.read())


def cleanup():
    if os.path.exists(f"{BASE_PATH}/data/foundation"):
        shutil.rmtree(f"{BASE_PATH}/data/foundation")


def test_cnv():
    cleanup()
    os.makedirs(f"{BASE_PATH}/data/SA-1612348", exist_ok=True)

    xml = read_xml(f"{BASE_PATH}/data/sample.xml")

    mock_log = MockLog()

    extract_copy_numbers(
        xml["rr:ResultsReport"]["rr:ResultsPayload"],
        "SA-1612348",
        f"{BASE_PATH}/data",
        mock_log,
    )

    csv = open(f"{BASE_PATH}/data/sample/sample.copynumber.csv")
    text = csv.read()
    csv.close()

    assert (
        text
        == """sample_id,gene,copy_number,status,attributes,chromosome,start_position,end_position,interpretation
SA-1612348,CDK4,44.0,amplification,"{'number-of-exons': '7 of 7', 'status': 'amplification', 'ratio': '11.63', 'interpretation': 'known'}",chr12,58093932,58188144,Pathogenic
SA-1612348,CCND3,6.0,gain,"{'number-of-exons': '5 of 5', 'status': 'amplification', 'ratio': '2.17', 'interpretation': 'known'}",chr6,41853880,41956362,Pathogenic
SA-1612348,MYC,41.0,amplification,"{'number-of-exons': '5 of 5', 'status': 'amplification', 'ratio': '10.34', 'interpretation': 'known'}",chr8,128706589,128801451,Pathogenic
SA-1612348,PIM1,6.0,gain,"{'number-of-exons': '7 of 7', 'status': 'amplification', 'ratio': '2.14', 'interpretation': 'unknown'}",chr6,37138078,37141867,Uncertain significance
SA-1612348,RAD21,7.0,gain,"{'number-of-exons': '13 of 13', 'status': 'amplification', 'ratio': '2.69', 'interpretation': 'unknown'}",chr8,117859738,117878968,Uncertain significance
"""
    )


def test_fnv():
    cleanup()
    os.makedirs(f"{BASE_PATH}/data/SA-1612348", exist_ok=True)

    xml = read_xml(f"{BASE_PATH}/data/sample.xml")

    mock_log = MockLog()

    extract_fusion_variant(
        xml["rr:ResultsReport"]["rr:ResultsPayload"],
        "SA-1612348",
        f"{BASE_PATH}/data",
        mock_log,
    )

    with open(f"{BASE_PATH}/data/sample/sample.structural.csv", newline="") as test_in:
        csv_reader = csv.reader(test_in)
        test_data = list(csv_reader)
        # Check header is correct
        assert (
            ",".join(test_data[0])
            == "sample_id,gene1,gene2,effect,chromosome1,start_position1,end_position1,chromosome2,start_position2,end_position2,interpretation,sequence_type,in-frame,attributes"
        )
        # Check when both chromosomes are given ranges
        assert (
            ",".join(test_data[1])
            == "SA-1612348,NF1,N/A,truncation,chr17,29557687,29887856,chr6,66426718,66427149,Likely pathogenic,somatic,unknown,{'equivocal': 'false', 'supporting-read-pairs': '83'}"
        )
        # Check when single loci, different chromosomes
        assert (
            ",".join(test_data[2])
            == "SA-1612348,NF1,FN2,fusion,chr17,29557687,29557687,chr6,66426718,66426718,Likely pathogenic,somatic,unknown,{'equivocal': 'false', 'supporting-read-pairs': '83'}"
        )
        # Check when single loci, same chromosome
        assert (
            ",".join(test_data[3])
            == "SA-1612348,FN2,NF1,rearrangement,chr17,29557687,29557687,chr17,29557790,29557790,Likely pathogenic,somatic,unknown,{'equivocal': 'false', 'supporting-read-pairs': '83'}"
        )


def test_yml():
    cleanup()
    os.makedirs(f"{BASE_PATH}/data/SA-1612348", exist_ok=True)

    xml = read_xml(f"{BASE_PATH}/data/sample.xml")

    yml = get_test_yml(
        xml["rr:ResultsReport"]["rr:CustomerInformation"],
        xml["rr:ResultsReport"]["rr:ResultsPayload"],
        "SA-1612348",
        f"{BASE_PATH}/data",
        None,
        True,
        ".lifeomic/foundation",
        "sourceFileId",
    )

    assert yml == {
        "name": "Foundation Medicine",
        "reference": "GRCh37",
        "sourceFileId": "sourceFileId",
        "testType": "FoundationOne Heme",
        "indexedDate": "2016-07-15",
        "receivedDate": "2016-07-21",
        "collDate": "2016-07-15",
        "reportDate": "2016-08-25",
        "mrn": "12345678",
        "reportID": "SMP37669",
        "patientDOB": "2002-12-12",
        "patientLastName": "Patient",
        "medFacilName": "ABC Oncology",
        "medFacilID": "200313",
        "orderingMDName": "Smith, John",
        "orderingMDNPI": "1508888051",
        "bodySite": "Bone",
        "bodySiteSystem": "http://lifeomic.com/fhir/sequence-body-site",
        "bodySiteDisplay": "Bone",
        "indication": "PEDIATRIC Bone osteosarcoma",
        "indicationDisplay": "PEDIATRIC Bone osteosarcoma",
        "indicationSystem": "http://lifeomic.com/fhir/sequence-indication",
        "files": [
            {
                "type": "copyNumberVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.copynumber.csv",
            },
            {
                "type": "structuralVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.structural.csv",
            },
            {
                "type": "shortVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.nrm.vcf.gz",
            },
        ],
        "patientInfo": {
            "firstName": "Test",
            "lastName": "Patient",
            "gender": "male",
            "dob": "2002-12-12",
            "identifiers": [
                {
                    "codingSystem": "http://hl7.org/fhir/v2/0203",
                    "codingCode": "MR",
                    "value": "12345678",
                }
            ],
        },
        "lossOfHeterozygosityScore": 21.1,
        "lossOfHeterozygosityStatus": "high",
        "msi": "stable",
        "tmb": "low",
        "tmbScore": 0.73,
        "nonHumanContent": [
            {"nhcOrganism": "HHV-4", "nhcReadsPerMil": 14.0, "nhcStatus": "unknown"}
        ],
        "plasmaTumorFraction": "Not Elevated",
    }


def test_yml_with_date_namespace():
    cleanup()
    os.makedirs(f"{BASE_PATH}/data/SA-1612348", exist_ok=True)

    xml = read_xml(f"{BASE_PATH}/data/sample_namespace.xml")

    yml = get_test_yml(
        xml["rr:ResultsReport"]["rr:CustomerInformation"],
        xml["rr:ResultsReport"]["rr:ResultsPayload"],
        "SA-1612348",
        f"{BASE_PATH}/data",
        None,
        True,
        ".lifeomic/foundation",
        "sourceFileId",
    )

    assert yml == {
        "name": "Foundation Medicine",
        "reference": "GRCh37",
        "sourceFileId": "sourceFileId",
        "testType": "FoundationOne Heme",
        "indexedDate": "2016-07-15",
        "receivedDate": "2016-07-21",
        "collDate": "2016-07-15",
        "reportDate": "2016-08-25",
        "mrn": "12345678",
        "reportID": "SMP37669",
        "patientDOB": "2002-12-12",
        "patientLastName": "Patient",
        "medFacilName": "ABC Oncology",
        "medFacilID": "200313",
        "orderingMDName": "Smith, John",
        "orderingMDNPI": "1508888051",
        "bodySite": "Bone",
        "bodySiteSystem": "http://lifeomic.com/fhir/sequence-body-site",
        "bodySiteDisplay": "Bone",
        "indication": "PEDIATRIC Bone osteosarcoma",
        "indicationDisplay": "PEDIATRIC Bone osteosarcoma",
        "indicationSystem": "http://lifeomic.com/fhir/sequence-indication",
        "files": [
            {
                "type": "copyNumberVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.copynumber.csv",
            },
            {
                "type": "structuralVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.structural.csv",
            },
            {
                "type": "shortVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.nrm.vcf.gz",
            },
        ],
        "patientInfo": {
            "firstName": "Test",
            "lastName": "Patient",
            "gender": "male",
            "dob": "2002-12-12",
            "identifiers": [
                {
                    "codingSystem": "http://hl7.org/fhir/v2/0203",
                    "codingCode": "MR",
                    "value": "12345678",
                }
            ],
        },
        "lossOfHeterozygosityScore": -1,
        "lossOfHeterozygosityStatus": "high",
        "msi": "stable",
        "tmb": "low",
        "tmbScore": 0.73,
    }


def test_vcf_etl():
    vcf_actual_lines = []
    vcf_expected_lines = []

    vcf_etl(f"{BASE_PATH}/data/sample.vcf", f"{BASE_PATH}/data/sample/sample.vcf", "SAMPLE")

    with open(f"{BASE_PATH}/data/vcf_expected.vcf") as f:
        vcf_expected_lines = f.readlines()

    with gzip.open(f"{BASE_PATH}/data/sample/sample.vcf.gz", "rt") as f:
        vcf_actual_lines = f.readlines()

    # unlike the gzip CLI tool, gzip.open leaves the input files intact, so reset the files
    with open(f"{BASE_PATH}/data/sample/sample.vcf", "w") as f:
        f.writelines(vcf_actual_lines)
    os.remove(f"{BASE_PATH}/data/sample/sample.vcf.gz")

    # lets make sure we actual read lines
    assert len(vcf_actual_lines) == 27
    # verifying that all lines in the unzipped vcf match the expected vcf
    for idx, val in enumerate(vcf_expected_lines):
        assert val == vcf_actual_lines[idx]


def test_vcf_with_scientific_notation_etl():
    vcf_actual_lines = []
    vcf_expected_lines = []

    vcf_etl(
        f"{BASE_PATH}/data/sample_scientific_notation.vcf",
        f"{BASE_PATH}/data/sample_scientific_notation/sample_scientific_notation.vcf",
        "SAMPLE",
    )

    with open(f"{BASE_PATH}/data/vcf_expected_scientific_notation.vcf") as f:
        vcf_expected_lines = f.readlines()

    with gzip.open(
        f"{BASE_PATH}/data/sample_scientific_notation/sample_scientific_notation.vcf.gz", "rt"
    ) as f:
        vcf_actual_lines = f.readlines()

    # unlike the gzip CLI tool, gzip.open leaves the input files intact, so reset the files
    with open(
        f"{BASE_PATH}/data/sample_scientific_notation/sample_scientific_notation.vcf", "w"
    ) as f:
        f.writelines(vcf_actual_lines)
    os.remove(f"{BASE_PATH}/data/sample_scientific_notation/sample_scientific_notation.vcf.gz")

    # lets make sure we actual read lines
    assert len(vcf_actual_lines) == 28
    # verifying that all lines in the unzipped vcf match the expected vcf
    for idx, val in enumerate(vcf_expected_lines):
        assert val == vcf_actual_lines[idx]


def test_transform_scientific_notation_in_af():
    line_with_scientific_notation = "chr17	41228516	.	TG	T	.	PASS	AF=9.771078E-4;cds_syntax=4472delC;cosmic_status=LIKELY;depth=3087;effect=FRAMESHIFT;gene_name=BRCA1;protein_syntax=P1491fs*14;transcript_name=NM_007294"
    expected_line_with_scientific_notation = "chr17	41228516	.	TG	T	.	PASS	AF=0.0009771078;cds_syntax=4472delC;cosmic_status=LIKELY;depth=3087;effect=FRAMESHIFT;gene_name=BRCA1;protein_syntax=P1491fs*14;transcript_name=NM_007294"

    line_without_scientific_notation = "chr6	117710838	.	C	A	.	PASS	AF=0.4173;cds_syntax=1434G>T;cosmic_status=UNKNOWN;depth=1385;effect=MISSENSE;gene_name=ROS1;protein_syntax=M478I;transcript_name=NM_002944"

    # confirm we alter the scientific notation correctly
    transformed_line_with_scientific_notation = transform_scientific_notation_in_af(
        line_with_scientific_notation
    )
    assert expected_line_with_scientific_notation == transformed_line_with_scientific_notation

    # confirm we don't alter lines without scientific notation at all
    transformed_line_without_scientific_notation = transform_scientific_notation_in_af(
        line_without_scientific_notation
    )
    assert line_without_scientific_notation == transformed_line_without_scientific_notation


def test_yml_with_missing_mrn():
    cleanup()
    os.makedirs(f"{BASE_PATH}/data/SA-1612348", exist_ok=True)

    xml = read_xml(f"{BASE_PATH}/data/sample_missing_mrn.xml")

    yml = get_test_yml(
        xml["rr:ResultsReport"]["rr:CustomerInformation"],
        xml["rr:ResultsReport"]["rr:ResultsPayload"],
        "SA-1612348",
        f"{BASE_PATH}/data",
        None,
        True,
        ".lifeomic/foundation",
        "sourceFileId",
    )

    assert yml == {
        "name": "Foundation Medicine",
        "reference": "GRCh37",
        "sourceFileId": "sourceFileId",
        "testType": "FoundationOne Heme",
        "indexedDate": "2016-07-15",
        "receivedDate": "2016-07-21",
        "collDate": "2016-07-15",
        "reportDate": "2016-08-25",
        "mrn": "",
        "reportID": "SMP37669",
        "patientDOB": "2002-12-12",
        "patientLastName": "Patient",
        "medFacilName": "ABC Oncology",
        "medFacilID": "200313",
        "orderingMDName": "Smith, John",
        "orderingMDNPI": "1508888051",
        "bodySite": "Bone",
        "bodySiteSystem": "http://lifeomic.com/fhir/sequence-body-site",
        "bodySiteDisplay": "Bone",
        "indication": "PEDIATRIC Bone osteosarcoma",
        "indicationDisplay": "PEDIATRIC Bone osteosarcoma",
        "indicationSystem": "http://lifeomic.com/fhir/sequence-indication",
        "files": [
            {
                "type": "copyNumberVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.copynumber.csv",
            },
            {
                "type": "structuralVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.structural.csv",
            },
            {
                "type": "shortVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.nrm.vcf.gz",
            },
        ],
        "patientInfo": {
            "firstName": "Test",
            "lastName": "Patient",
            "gender": "male",
            "dob": "2002-12-12",
        },
        "lossOfHeterozygosityScore": -1,
        "lossOfHeterozygosityStatus": "high",
        "msi": "stable",
        "tmb": "low",
        "tmbScore": 0.73,
    }


def test_yml_with_no_biomarkers():
    cleanup()
    os.makedirs(f"{BASE_PATH}/data/SA-1612348", exist_ok=True)

    xml = read_xml(f"{BASE_PATH}/data/sample_no_biomarkers.xml")

    yml = get_test_yml(
        xml["rr:ResultsReport"]["rr:CustomerInformation"],
        xml["rr:ResultsReport"]["rr:ResultsPayload"],
        "SA-1612348",
        f"{BASE_PATH}/data",
        None,
        True,
        ".lifeomic/foundation",
        "sourceFileId",
    )

    assert yml == {
        "name": "Foundation Medicine",
        "reference": "GRCh37",
        "sourceFileId": "sourceFileId",
        "testType": "FoundationOne Heme",
        "indexedDate": "2016-07-15",
        "receivedDate": "2016-07-21",
        "collDate": "2016-07-15",
        "reportDate": "2016-08-25",
        "mrn": "12345999",
        "reportID": "SMP37779",
        "patientDOB": "2002-04-12",
        "patientLastName": "Patient",
        "medFacilName": "ABC Oncology",
        "medFacilID": "200313",
        "orderingMDName": "Smith, John",
        "orderingMDNPI": "1508888051",
        "bodySite": "Bone",
        "bodySiteSystem": "http://lifeomic.com/fhir/sequence-body-site",
        "bodySiteDisplay": "Bone",
        "indication": "PEDIATRIC Bone osteosarcoma",
        "indicationDisplay": "PEDIATRIC Bone osteosarcoma",
        "indicationSystem": "http://lifeomic.com/fhir/sequence-indication",
        "files": [
            {
                "type": "copyNumberVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.copynumber.csv",
            },
            {
                "type": "structuralVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.structural.csv",
            },
            {
                "type": "shortVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.nrm.vcf.gz",
            },
        ],
        "patientInfo": {
            "firstName": "Nobiomarkers",
            "lastName": "Patient",
            "gender": "male",
            "dob": "2002-04-12",
            "identifiers": [
                {
                    "codingSystem": "http://hl7.org/fhir/v2/0203",
                    "codingCode": "MR",
                    "value": "12345999",
                }
            ],
        },
        "lossOfHeterozygosityScore": 21.1,
        "lossOfHeterozygosityStatus": "high",
    }


def test_yml_with_multiple_non_human_content():
    cleanup()
    os.makedirs(f"{BASE_PATH}/data/SA-1612348", exist_ok=True)

    xml = read_xml(f"{BASE_PATH}/data/sample_with_multiple_non_human_content.xml")

    yml = get_test_yml(
        xml["rr:ResultsReport"]["rr:CustomerInformation"],
        xml["rr:ResultsReport"]["rr:ResultsPayload"],
        "SA-1612348",
        f"{BASE_PATH}/data",
        None,
        True,
        ".lifeomic/foundation",
        "sourceFileId",
    )

    assert yml == {
        "name": "Foundation Medicine",
        "reference": "GRCh37",
        "sourceFileId": "sourceFileId",
        "testType": "FoundationOne Heme",
        "indexedDate": "2016-07-15",
        "receivedDate": "2016-07-21",
        "collDate": "2016-07-15",
        "reportDate": "2016-08-25",
        "mrn": "12345678",
        "reportID": "SMP37669",
        "patientDOB": "2002-12-12",
        "patientLastName": "Patient",
        "medFacilName": "ABC Oncology",
        "medFacilID": "200313",
        "orderingMDName": "Smith, John",
        "orderingMDNPI": "1508888051",
        "bodySite": "Bone",
        "bodySiteSystem": "http://lifeomic.com/fhir/sequence-body-site",
        "bodySiteDisplay": "Bone",
        "indication": "PEDIATRIC Bone osteosarcoma",
        "indicationDisplay": "PEDIATRIC Bone osteosarcoma",
        "indicationSystem": "http://lifeomic.com/fhir/sequence-indication",
        "files": [
            {
                "type": "copyNumberVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.copynumber.csv",
            },
            {
                "type": "structuralVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.structural.csv",
            },
            {
                "type": "shortVariant",
                "sequenceType": "somatic",
                "fileName": ".lifeomic/foundation/SA-1612348/SA-1612348.nrm.vcf.gz",
            },
        ],
        "patientInfo": {
            "firstName": "Test",
            "lastName": "Patient",
            "gender": "male",
            "dob": "2002-12-12",
            "identifiers": [
                {
                    "codingSystem": "http://hl7.org/fhir/v2/0203",
                    "codingCode": "MR",
                    "value": "12345678",
                }
            ],
        },
        "lossOfHeterozygosityScore": 21.1,
        "lossOfHeterozygosityStatus": "high",
        "msi": "stable",
        "tmb": "low",
        "tmbScore": 0.73,
        "nonHumanContent": [
            {"nhcOrganism": "HHV-4", "nhcReadsPerMil": 14.0, "nhcStatus": "unknown"},
            {"nhcOrganism": "HPV-18", "nhcReadsPerMil": 17.0, "nhcStatus": "unknown"},
            {"nhcOrganism": "HHV-4", "nhcReadsPerMil": 92.0, "nhcStatus": "unknown"},
        ],
    }


def test_get_mrn():
    missing_mrn_result = get_mrn({"LastName": "Baggins"})
    assert missing_mrn_result == ""

    existing_mrn_result = get_mrn({"LastName": "Baggins", "MRN": "mrn_001"})
    assert existing_mrn_result == "mrn_001"


def test_get_trf():
    missing_trf = get_trf({"LastName": "Baggins"})
    assert missing_trf == ""

    existing_trf = get_trf({"LastName": "Baggins", "TRFNumber": "SMP102938"})
    assert existing_trf == "SMP102938"


def test_get_med_facil():
    missing_med_facil_ID = get_med_facil({"MedFacilName": "ABC Oncology", "MedFacilID": ""})
    assert missing_med_facil_ID == ["ABC Oncology", ""]

    missing_med_facil_name = get_med_facil({"MedFacilName": "", "MedFacilID": "200313"})
    assert missing_med_facil_name == ["", "200313"]

    missing_med_facil_both = get_med_facil({"MedFacilName": "", "MedFacilID": ""})
    assert missing_med_facil_both == ["", ""]

    existing_med_facil_both = get_med_facil(
        {"MedFacilName": "ABC Oncology", "MedFacilID": "200313"}
    )
    assert existing_med_facil_both == ["ABC Oncology", "200313"]


def test_get_ordering_md():
    missing_md_NPI = get_ordering_md({"OrderingMD": "Smith, John"}, "")
    assert missing_md_NPI == ["Smith, John", ""]

    missing_md_name = get_ordering_md({"OrderingMD": ""}, "9706")
    assert missing_md_name == ["", "9706"]

    missing_md_both = get_ordering_md({"OrderingMD": ""}, "")
    assert missing_md_both == ["", ""]

    existing_md_both = get_ordering_md({"OrderingMD": "Smith, John"}, "9706")
    assert existing_md_both == ["Smith, John", "9706"]


def test_get_non_human_content():
    single_nhc = get_non_human_content(
        [{"@organism": "HHV-4", "@reads-per-million": "14", "@status": "unknown"}]
    )
    assert single_nhc == [{"nhcOrganism": "HHV-4", "nhcReadsPerMil": 14, "nhcStatus": "unknown"}]

    multiple_nhc = get_non_human_content(
        [
            {"@organism": "HHV-4", "@reads-per-million": "14", "@status": "unknown"},
            {"@organism": "HPV-4", "@reads-per-million": "24", "@status": "unknown"},
        ]
    )
    assert multiple_nhc == [
        {"nhcOrganism": "HHV-4", "nhcReadsPerMil": 14.0, "nhcStatus": "unknown"},
        {"nhcOrganism": "HPV-4", "nhcReadsPerMil": 24.0, "nhcStatus": "unknown"},
    ]

    no_organism = get_non_human_content([{"@reads-per-million": "14", "@status": "unknown"}])
    assert no_organism == [{"nhcOrganism": "unknown", "nhcReadsPerMil": 14, "nhcStatus": "unknown"}]

    no_rpm = get_non_human_content([{"@organism": "HHV-4", "@status": "unknown"}])
    assert no_rpm == [{"nhcOrganism": "HHV-4", "nhcReadsPerMil": 0.0, "nhcStatus": "unknown"}]

    no_status = get_non_human_content([{"@organism": "HHV-4", "@reads-per-million": "14"}])
    assert no_status == [{"nhcOrganism": "HHV-4", "nhcReadsPerMil": 14, "nhcStatus": "unknown"}]


def test_get_plasma_tumor_fraction():
    ptf_elevated = get_plasma_tumor_fraction(
        {
            "Gene": [
                {
                    "Name": "Tumor Fraction",
                    "Include": "true",
                    "Alterations": {
                        "Alteration": {
                            "Name": "Elevated Tumor Fraction",
                            "AlterationProperties": {
                                "AlterationProperty": {
                                    "@isEquivocal": "false",
                                    "@name": "Elevated Tumor Fraction",
                                }
                            },
                            "Interpretation": "Tumor fraction provides an estimate of the percentage...",
                            "Include": "true",
                            "ClinicalTrialNote": None,
                            "Therapies": None,
                            "ReferenceLinks": None,
                            "ClinicalTrialLinks": None,
                        }
                    },
                    "ReferenceLinks": None,
                }
            ]
        }
    )

    assert ptf_elevated == "Elevated"

    ptf_not_elevated = get_plasma_tumor_fraction(
        {
            "Gene": [
                {
                    "Name": "Tumor Fraction",
                    "Include": "true",
                    "Alterations": {
                        "Alteration": {
                            "Name": "Elevated Tumor Fraction Not Detected",
                            "AlterationProperties": {
                                "AlterationProperty": {
                                    "@isEquivocal": "false",
                                    "@name": "Elevated Tumor Fraction Not Detected",
                                }
                            },
                            "Interpretation": "Tumor fraction provides an estimate of the percentage...",
                            "Include": "true",
                            "ClinicalTrialNote": None,
                            "Therapies": None,
                            "ReferenceLinks": None,
                            "ClinicalTrialLinks": None,
                        }
                    },
                    "ReferenceLinks": None,
                }
            ]
        }
    )

    assert ptf_not_elevated == "Not Elevated"

    ptf_undetermined = get_plasma_tumor_fraction(
        {
            "Gene": [
                {
                    "Name": "Tumor Fraction",
                    "Include": "true",
                    "Alterations": {
                        "Alteration": {
                            "Name": "Cannot Be Determined",
                            "AlterationProperties": {
                                "AlterationProperty": {
                                    "@isEquivocal": "false",
                                    "@name": "Cannot Be Determined",
                                }
                            },
                            "Interpretation": "Tumor fraction provides an estimate of the percentage...",
                            "Include": "true",
                            "ClinicalTrialNote": None,
                            "Therapies": None,
                            "ReferenceLinks": None,
                            "ClinicalTrialLinks": None,
                        }
                    },
                    "ReferenceLinks": None,
                }
            ]
        }
    )

    assert ptf_undetermined == "Undetermined"

    ptf_absent = get_plasma_tumor_fraction(
        {
            "Gene": [
                {
                    "Name": "MYC",
                    "Include": "true",
                    "Alterations": {
                        "Alteration": {
                            "Name": "amplification",
                            "AlterationProperties": {
                                "AlterationProperty": {
                                    "@isEquivocal": "false",
                                    "@isSubclonal": "false",
                                    "@name": "amplification",
                                }
                            },
                            "Interpretation": "MYC (c-MYC) encodes a transcription factor that regulates several genes related to cell cycle regulation and cell growth. It is an oncogene and may be activated in as many as 20% of cancers (Dang et al., 2006; 16904903). MYC deregulation (amplification, overexpression, translocation) has been identified in a number of different cancer types (Nesbit et al., 1999; 10378696). MYC amplification has been significantly linked with increased mRNA and protein levels and results in the dysregulation of a large number of target genes (Blancato et al., 2004; 15083194, Dang et al., 2006; 16904903, Fromont et al., 2013; 23574779). MYC amplification has been reported in 16% of osteosarcoma cases and has been significantly associated with poor prognosis (Smida et al., 2010; 20610556). In osteosarcoma, MYC amplification has been observed frequently with alterations of RB1 (Smida et al., 2010; 20610556). c-Myc expression has been observed in up to 86% (48/56) of osteosarcomas, and has also been correlated with a poor prognosis (Wu et al., 2012; 21890444). There are no available therapies that directly target MYC. However, preclinical studies have suggested several synthetic lethal strategies to indirectly target MYC; these studies have shown that cells that overexpress MYC protein may be sensitive to CDK1, CDK2, or Aurora kinase B inhibitors, including those that are under investigation in clinical trials (Horiuchi et al., 2012; 22430491, Hook et al., 2012; 22222631, Goga et al., 2007; 17589519, Yang et al., 2010; 20643922, Molenaar et al., 2009; 19525400). A patient with MYC-amplified invasive ductal breast carcinoma experienced a partial response to an Aurora kinase inhibitor (Ganesan et al., 2014; 25253784). Furthermore, in numerous preclinical studies, inhibition of BET bromodomain-containing proteins, in particular BRD4, has been reported to downregulate MYC expression and MYC-dependent gene expression programs in a variety of hematopoietic and solid tumor cancer models and primary cells (Delmore et al., 2011; 21889194, Bandopadhayay et al., 2013; 24297863, Loven et al., 2013; 23582323). Phase 1 trials of the BET inhibitor OTX015 in patients with hematological malignancies reported clinical activity in patients with acute myeloid leukemia (AML) or lymphoma (Herait et al., 2015; TAT Abstract O7.3, Dombret et al., 2014; ASH Abstract 117, Thieblemont et al., 2014; ASH Abstract 4417). On the basis of preclinical (Sun et al., 2016; AACR Abstract 4634)(Dong et al., 2013; 23866964, Pei et al., 2016; 26977882) and limited clinical (Younes et al., 2015; ASH Abstract 257)(Younes et al., 2016; 27049457) data, MYC alterations that lead to increased expression of MYC may predict sensitivity to combinatorial inhibition of HDAC and PI3K in diffuse large B-cell lymphoma (DLBCL); it is not clear whether this approach would be beneficial in other cancer types. MYC amplification has also been suggested to predict response to chemotherapy in patients with breast cancer in some studies (Pereira et al., 2013; 23555992, Yasojima et al., 2011; 21741827). Preclinical evidence suggests that colon cancer cells with MYC amplification may be more sensitive to 5-fluorouracil and paclitaxel (Arango et al., 2001; 11406570, Bottone et al., 2003; 14516787).",
                            "Include": "true",
                            "ClinicalTrialNote": None,
                            "Therapies": None,
                            "ReferenceLinks": None,
                            "ClinicalTrialLinks": None,
                        }
                    },
                    "ReferenceLinks": None,
                }
            ]
        }
    )

    assert ptf_absent == None
