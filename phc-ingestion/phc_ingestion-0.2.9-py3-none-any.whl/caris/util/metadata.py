import pandas as pd
import numpy as np
import re
from logging import Logger

MSI_MAPPINGS = {
    "low": "low",
    "stable": "stable",
    "high": "high",
    "indeterminate": "indeterminate",
    "equivocal": "indeterminate",
}


def get_received_date(specimen_details) -> str:
    return specimen_details.get("specimenReceivedDate", "")


def get_collected_date(specimen_details) -> str:
    return specimen_details.get("specimenCollectionDate", "")


def get_report_date(test_details, log: Logger) -> str:
    try:
        test_details["approvalInformation"]["approveDate"].split()[0]
    except KeyError:
        log.info("JSON does not contain approval information")
        return ""

    else:
        return test_details["approvalInformation"]["approveDate"].split()[0]


def get_ordering_md_name(physician_details) -> str:
    return (
        f'{physician_details["lastName"]}, {physician_details["firstName"]}'
        if physician_details.get("lastName") and physician_details.get("firstName")
        else ""
    )


def get_ordering_md_npi(physician_details) -> int:
    return physician_details.get("npi", "")


def get_med_facil_name(physician_details) -> str:
    return physician_details.get("organization", "")


def get_med_facil_id(physician_details) -> int:
    return physician_details.get("sourceID", "")


def get_report_id(test_details) -> str:
    return test_details.get("labReportID", "")


def get_physician_details(data) -> dict:
    return data.get("physicianInformation", {})


def get_ihc_results(data, log) -> list:
    # Initialize trigger for logging, and a results list
    trigger = False
    ihc_results = []

    try:
        ihc_tests = [test for test in data.get("tests") if test["testMethodology"] == "IHC"]
    except TypeError:
        log.info("No Immunohistochemistry tests reported")
        return ihc_results

    hidden_ic = re.compile(r"[IC]")

    for test in ihc_tests:
        test_results = test["testResults"]["expressionAlteration"]

        biomarkername = test_results.get("biomarkerName", "")
        result = test_results.get("result", "")

        # Grab a field prefix list to hunt for tc / ic fields
        prefix_list = [x[:2] for x in list(test_results)]
        # If ic / tc counts are off, log it and try to load in minimal test info for future troubleshooting
        if 0 < (prefix_list.count("tc") + prefix_list.count("ic")) < 7:
            log.warning(
                f'IHC test {test_results["biomarkerName"]} has an unexpected pattern: ic/tc field count is {prefix_list.count("tc")+prefix_list.count("ic")}. Should be 0 or 7(PD-L1).'
            )
            trigger = True
            ihc_results.append({"biomarkerName": biomarkername, "result": result})

        # Check for PD-L1 tests, work through odd handling patterns
        elif test_results["biomarkerName"][:5] == "PD-L1":
            # Tumor cell / immune cell logic
            if prefix_list.count("tc") == 4 and prefix_list.count("ic") == 3:
                tc_result = test_results.get("tcResult", "")
                tc_intensity = test_results.get("tcIntensity", "")
                tc_stainpercent = test_results.get("tcStainPercent", np.nan)
                tc_threshold = (
                    test_results["tcThreshold"].split("or")[-1].strip()
                    if test_results.get("tcThreshold")
                    else ""
                )
                ic_result = test_results.get("icResult", "")
                ic_stainpercent = test_results.get("icStainPercent", np.nan)

                ic_threshold = (
                    test_results["icThreshold"].split("or")[0].strip()
                    if test_results.get("icThreshold")
                    else ""
                )

                ihc_results.append(
                    {
                        "biomarkerName": biomarkername,
                        "result": result,
                        "tcResult": tc_result,
                        "tcIntensity": tc_intensity,
                        "tcStainPercent": float(tc_stainpercent),
                        "tcThreshold": tc_threshold,
                        "icResult": ic_result,
                        "icStainPercent": float(ic_stainpercent),
                        "icThreshold": ic_threshold,
                    }
                )
            # PD-L1 (22c3) tests report a cpScore, and no stain or intensity metrics
            elif test_results["biomarkerName"][-6:] == "(22c3)":
                cpScore = test_results.get("cpScore", np.nan)

                threshold = (
                    test_results["threshold"].split("or")[-1].strip()
                    if test_results.get("threshold")
                    else ""
                )
                ihc_results.append(
                    {
                        "biomarkerName": biomarkername,
                        "result": result,
                        "cpScore": float(cpScore),
                        "threshold": threshold,
                    }
                )

                # Check if correct pattern is followed
                # stainPercent and intensity fields should be missing
                if test_results.get("intensity"):
                    if test_results["intensity"] != "":
                        log.warning(
                            f'IHC test {test_results["biomarkerName"]} has an unexpected pattern for "intensity": value of "{test_results["intensity"]}" was given when None was expected'
                        )
                        trigger = True
                if test_results.get("stainPercent"):
                    if np.isnan(test_results["stainPercent"]) == False:
                        log.warning(
                            f'IHC test {test_results["biomarkerName"]} has an unexpected pattern for "stainPercent": value of "{test_results["stainPercent"]}" was given when None was expected'
                        )
                        trigger = True

            # Some PD-L1 tests don't have icThreshold field filled out,
            # but report IC Threshold in the regualr Threshold field
            elif isinstance((re.search(hidden_ic, test_results["threshold"])), re.Match):
                stainpercent = test_results.get("stainPercent", np.nan)

                # IC grabs threshold from the front
                threshold = (
                    test_results["threshold"].split("or")[0].strip()
                    if test_results.get("threshold")
                    else ""
                )

                ihc_results.append(
                    {
                        "biomarkerName": biomarkername,
                        "result": result,
                        "stainPercent": float(stainpercent),
                        "threshold": threshold,
                    }
                )

                # Check if correct pattern is followed
                # Intensity field should be missing
                if test_results.get("intensity"):
                    if test_results["intensity"] != "":
                        log.warning(
                            f'IHC test {test_results["biomarkerName"]} has an unexpected pattern for "intensity": value of "{test_results["intensity"]}" was given when None was expected'
                        )
                        trigger = True

            # If no PD-L1 oddities are found, then report PD-L1 as a standard test
            else:
                intensity = test_results.get("intensity")
                stainpercent = test_results.get("stainPercent", np.nan)
                threshold = (
                    test_results["threshold"].split("or")[-1].strip()
                    if test_results.get("threshold")
                    else ""
                )

                ihc_results.append(
                    {
                        "biomarkerName": biomarkername,
                        "result": result,
                        "intensity": intensity,
                        "stainPercent": float(stainpercent),
                        "threshold": threshold,
                    }
                )

        # Mismatch Repair Status only reports biomarker and result
        elif test_results["biomarkerName"] == "Mismatch Repair Status":
            ihc_results.append({"biomarkerName": biomarkername, "result": result})
            # Check if correct pattern is followed
            # stainPercent, intensity and threshold fields should be missing
            if test_results.get("intensity"):
                if test_results["intensity"] != "":
                    log.warning(
                        f'IHC test {test_results["biomarkerName"]} has an unexpected pattern for "intensity": value of "{test_results["intensity"]}" was given when None was expected'
                    )
                    trigger = True
            if test_results.get("stainPercent"):
                if np.isnan(test_results["stainPercent"]) == False:
                    log.warning(
                        f'IHC test {test_results["biomarkerName"]} has an unexpected pattern for "stainPercent": value of "{test_results["stainPercent"]}" was given when None was expected'
                    )
                    trigger = True
            if test_results.get("threshold"):
                if test_results["threshold"] != "":
                    log.warning(
                        f'IHC test {test_results["biomarkerName"]} has an unexpected pattern for "threshold": value of "{test_results["threshold"]}" was given when None was expected'
                    )
                    trigger = True

        # Standard test reporting
        else:
            intensity = test_results.get("intensity", "")
            stainpercent = test_results.get("stainPercent", np.nan)
            threshold = (
                test_results["threshold"].split("or")[-1].strip()
                if test_results.get("threshold")
                else ""
            )

            ihc_results.append(
                {
                    "biomarkerName": biomarkername,
                    "result": result,
                    "intensity": intensity,
                    "stainPercent": float(stainpercent),
                    "threshold": threshold,
                }
            )

    log.info(f"Immunohistochemistry tests detected: {len(ihc_results)}")

    # Missing field pattern checking
    for test in ihc_results:
        for k, v in test.items():
            # Log if any expected fields are left blank
            if k == "cpScore" or k == "stainPercent":
                if np.isnan(v):
                    log.warning(
                        f'IHC test {test["biomarkerName"]} has an unexpected pattern for field: {k}'
                    )
                    trigger = True

            else:
                if v == "":
                    log.warning(
                        f'IHC test {test["biomarkerName"]} has an unexpected pattern for field: {k}'
                    )
                    trigger = True

    if trigger == False:
        log.info("All IHC tests matched the expected patterns.")

    return ihc_results


# Build up the manifest iteratively because almost everything is optional
def extract_metadata(data, prefix, files, source_file_id, ingest_status, log: Logger):

    metadata = {}

    test_details = data["testDetails"]
    specimen_details = data["specimenInformation"]["tumorSpecimenInformation"]

    physician_details = get_physician_details(data)

    metadata["testType"] = "MI Profile"

    #  Get the date without the time
    metadata["indexedDate"] = test_details["receivedDate"].split()[0]

    # Get date of collected and received for the specimen
    metadata["receivedDate"] = get_received_date(specimen_details)
    metadata["collDate"] = get_collected_date(specimen_details)
    metadata["reportDate"] = get_report_date(test_details, log)

    patient = data["patientInformation"]
    metadata["bodySiteSystem"] = "http://lifeomic.com/fhir/sequence-body-site"
    metadata["reportID"] = get_report_id(test_details)
    metadata["mrn"] = patient["mrn"]
    metadata["patientLastName"] = patient["lastName"]

    metadata["patientDOB"] = patient["dob"]

    # Get physician info - ordering name, NPI, and facility
    metadata["medFacilName"] = get_med_facil_name(physician_details)
    metadata["medFacilID"] = get_med_facil_id(physician_details)
    metadata["orderingMDName"] = get_ordering_md_name(physician_details)
    metadata["orderingMDNPI"] = get_ordering_md_npi(physician_details)

    metadata["indicationSystem"] = "http://lifeomic.com/fhir/sequence-indication"
    metadata["indication"] = patient["diagnosis"]
    metadata["indicationDisplay"] = metadata["indication"]

    metadata["bodySite"] = data["specimenInformation"]["tumorSpecimenInformation"]["specimenSite"]
    metadata["bodySiteDisplay"] = metadata["bodySite"]
    metadata["sourceFileId"] = source_file_id
    pdf = files["pdf"]
    metadata["reportFile"] = f".lifeomic/caris/{prefix}/{pdf}"

    # Some patients do not have an MRN
    patientInfo = (
        {
            "lastName": metadata["patientLastName"],
            "dob": metadata["patientDOB"],
            "firstName": patient["firstName"],
            "gender": patient["gender"].lower(),
            "identifiers": [
                {
                    "codingCode": "MR",
                    "codingSystem": "http://hl7.org/fhir/v2/0203",
                    "value": metadata["mrn"],
                }
            ],
        }
        if metadata["mrn"]
        else {
            "lastName": metadata["patientLastName"],
            "dob": metadata["patientDOB"],
            "firstName": patient["firstName"],
            "gender": patient["gender"].lower(),
        }
    )

    # Ensure no null entries
    metadata["patientInfo"] = {k: v for k, v in patientInfo.items() if v}
    metadata.update({"name": "Caris", "reference": "GRCh37"})

    # Now find the test information

    tests = data["tests"]

    msi = None
    tmb = None
    tmbScore = None
    ihc_run_count = 0
    tmbUnit = None

    i = 0
    # if not sufficient quantity we won't have test results
    if test_details["reportType"] != "QNS":
        for test in tests:
            if (
                "clinical genes" in test["testName"].lower()
                and "test_cancellation_reason" not in test.keys()
                and test["testMethodology"] == "Seq"
            ):
                # They don't always do exome sequencing
                ingest_status["exome_performed"] = True
                for info in test["testResults"]:
                    if "tumorMutationBurden" in info.keys():
                        tmb = info["tumorMutationBurden"]["mutationBurdenCall"].lower()
                        tmbScore = info["tumorMutationBurden"]["mutationBurdenScore"]
                        if not tmbScore:
                            continue
                        tmbUnit = info["tumorMutationBurden"]["mutationBurdenUnit"]
                        # Convert from their format, which is "21 per Mb"
                        if tmbUnit == "Mutations/Megabase":
                            if ">150" in tmbScore:
                                tmbScore = 151.0
                            else:
                                tmbScore = float(tmbScore.split(" per")[0])
                        metadata["tmb"] = tmb
                        metadata["tmbScore"] = tmbScore
                    elif "microsatelliteInstability" in info.keys():
                        # if the key isn't found we will get an error during manifest processing
                        # it would be better to fail here, i.e. fail fast, but our alerting
                        # is much better at the manifest level so doing a default value for now
                        msi_key = info["microsatelliteInstability"]["msiCall"].lower()
                        if msi_key in MSI_MAPPINGS:
                            metadata["msi"] = MSI_MAPPINGS[msi_key]
                        else:
                            metadata["msi"] = msi_key
                    elif "genomicLevelHeterozygosity" in info.keys():
                        loh_status = info["genomicLevelHeterozygosity"]["result"].lower()
                        loh_score = info["genomicLevelHeterozygosity"]["LOHpercentage"]
                        # This comes out as a string, convert to integer for proper ingestion
                        metadata["lossOfHeterozygosityScore"] = int(loh_score)
                        metadata["lossOfHeterozygosityStatus"] = (
                            "qns" if loh_status == "quality not sufficient" else loh_status
                        )
            elif (
                "CNA" in test["testName"] or "CND" in test["testName"]
            ) and "test_cancellation_reason" not in test.keys():
                ingest_status["cnv_performed"] = True
                log.info(f"Copy Number Alteration testing identified: {test['testName']} ")
            elif (
                "Transcriptome" in test["testName"]
                and "test_cancellation_reason" not in test.keys()
            ):
                ingest_status["structural_performed"] = True
                log.info(f"Structural Variant testing identified: {test['testName']}")
            # elif ("PD-L1" in test['testName'] or "Mismatch Repair Status" in test['testName']) and 'test_cancellation_reason' not in test.keys():
            elif "IHC" in test["testMethodology"] and "test_cancellation_reason" not in test.keys():
                ingest_status["ihc_performed"] = True
                ihc_run_count += 1
                #  if ihc_run_count <=1:
                #      metadata['ihc']= immunohistochemistry(prefix, data)
                # log.info(f"IHC testing identified: {test['testName']}")
            i += 1

    # Add IHC test results to manifest
    metadata["ihcTests"] = get_ihc_results(data, log)

    # Add in the additional resources as linkable
    metadata["resources"] = []
    ingest_files = [
        "nrm.vcf.gz",
        "tmp",
        "ga4gh.genomics.yml",
        "runner",
        "yml",
        "ga4gh.yml",
        "copynumber.csv",
        "structural.csv",
    ]
    for ext, filename in files.items():
        if ext not in ingest_files:
            if ext != "bam" and "fastq" not in ext:
                metadata["resources"].append({"fileName": f".lifeomic/caris/{prefix}/{filename}"})
            else:
                for f in files[ext]:
                    metadata["resources"].append({"fileName": f".lifeomic/caris/{prefix}/{f}"})
                    if ext == "bam":
                        metadata["resources"].append(
                            {"fileName": f".lifeomic/caris/{prefix}/{f}.bai"}
                        )
            # If we got RNAseq results let us also make json files available
            if ext == "tsv":
                metadata["resources"].append(
                    {"fileName": f".lifeomic/caris/{prefix}/{prefix}.expression.cancerscope.json"}
                )
                metadata["resources"].append(
                    {"fileName": f".lifeomic/caris/{prefix}/{prefix}.expression.pcann.json"}
                )

    active_metadata = {k: v for k, v in metadata.items() if v is not None}
    return active_metadata
