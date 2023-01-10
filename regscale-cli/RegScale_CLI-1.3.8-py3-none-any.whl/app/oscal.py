#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

import dataclasses
import json
import sys
import tempfile
import uuid
from os import mkdir, path, remove, sep
from pathlib import Path
from subprocess import CalledProcessError, run

import click
import requests
import xmltodict
import yaml
from rich.progress import track

from app.api import Api
from app.application import Application
from app.logz import create_logger
from models.components import Component
from models.control_implementation import ControlImplementation

logger = create_logger()
app = Application()
config = app.config
oscal_cli_path = Path(config["oscal_cli_path"])
api = Api(app)


@click.group()
def oscal():
    """Performs bulk processing of OSCAL files"""


# OSCAL Version Support
@oscal.command()
def version():
    """Info on current OSCAL version supported by RegScale"""
    logger.info("RegScale currently supports OSCAL Version 1.0")
    check_oscal()


def convert_oscal_comp_to_regscale(j_data: dict) -> None:
    """Convert OSCAL component dict into a Regscale Component

    Args:
        j_data (dict): OSCAL component
    """
    component_id = None
    regscale_components = []
    components = []
    existing_components = api.get(
        url=config["domain"] + "/api/components/getList"
    ).json()
    controls_to_be_added = []
    j_data["component-definition"]["metadata"]
    try:
        components = j_data["component-definition"]["components"]
    except KeyError as kex:
        logger.error("Key Error! %s", kex)
        sys.exit(1)

    for comp in components:
        control_implementations = comp["control-implementations"]
        base_catalog = ""
        try:
            base_catalog = api.get(
                url=comp["control-implementations"][0]["source"], headers={}
            ).json()["catalog"]["metadata"]["title"]
        except requests.exceptions.RequestException as rex:
            logger.error(rex)
        except KeyError as kex:
            logger.error(kex)
        component = Component(
            title=comp["title"],
            componentOwnerId=app.config["userId"],
            componentType=comp["type"].lower(),
            description=comp["description"],
            purpose=comp["purpose"],
        )
        regscale_components.append(dataclasses.asdict(component))
        for control_implements in control_implementations:
            for control_data in control_implements["implemented-requirements"]:
                d = {
                    "title": control_data["control-id"],
                    "description": control_data["description"],
                }
                controls_to_be_added.append(d)
    for reg in regscale_components:

        check_component = [x for x in existing_components if x["title"] == reg["title"]]
        if not check_component:
            r = api.post(url=config["domain"] + "/api/components/", json=reg)
            if not r.raise_for_status():
                component_id = r.json()["id"]
                logger.info("Successfully posted %s to RegScale", reg["title"])
        else:
            for cmp in check_component:
                r = api.put(
                    url=config["domain"] + f"/api/components/{cmp['id']}", json=reg
                )
                if not r.raise_for_status():
                    component_id = cmp["id"]
                    # component_id = r.json()['id']
                    logger.info(
                        "Successfully updated component %s in RegScale", cmp["title"]
                    )
    # Load controls to RegScale and associate with new component
    load_controls(
        controls_to_be_added=controls_to_be_added,
        component_id=component_id,
        base_catalog=base_catalog,
    )


@oscal.command(name="component")
@click.argument("file_name", type=click.Path(exists=True))
def upload_component(file_name: str) -> None:
    """Upload OSCAL Component to RegScale.

    Args:
        file_name (str): Enter File Name
    """
    ## Load Controls and assign to component
    process_component(file_name=file_name)


def load_controls(
    controls_to_be_added: dict, component_id: int, base_catalog: str
) -> None:
    """Load control implementations to RegScale

    Args:
        controls_to_be_added (dict): _description_
        component_id (int): _description_
        base_catalog (str): _description_
    """
    control_implementations_to_insert = []
    control_implementations_to_update = []
    try:
        imp_r = api.get(
            url=config["domain"]
            + f"/api/controlImplementation/getAllByParent/{component_id}/components"
        )
        if not imp_r.raise_for_status():
            all_implementations = imp_r.json()
    except requests.RequestException as rex:
        logger.debug("no control implementations found for %s", component_id)
        all_implementations = []
    cats = api.get(url=config["domain"] + "/api/catalogues/getList").json()
    cat = [cat for cat in cats if cat["title"] == base_catalog]

    if len(cat) > 0:
        cat_id = cat[0]["id"]
        try:
            controls = api.get(
                config["domain"] + f"/api/SecurityControls/getList/{cat_id}"
            ).json()
        except requests.RequestException as rex:
            logger.error(rex)
            sys.exit(1)
        for imp_control in controls_to_be_added:
            try:
                reg_control = [
                    cntrl
                    for cntrl in controls
                    if cntrl["controlId"].lower() == imp_control["title"].lower()
                ]
                if len(reg_control) > 0:
                    control_implementation = ControlImplementation(
                        parentId=component_id,
                        parentModule="components",
                        controlOwnerId=config["userId"],
                        status="Fully Implemented",
                        controlID=reg_control[0]["id"],
                        implementation=imp_control["description"],
                    )
                    dat = dataclasses.asdict(control_implementation)
                    if control_implementation.implementation not in [
                        imp["implementation"]
                        for imp in all_implementations
                        if imp["implementation"]
                        == control_implementation.implementation
                    ]:
                        control_implementations_to_insert.append(dat)
                    else:
                        dat["id"] = [
                            imp["id"]
                            for imp in all_implementations
                            if imp["implementation"] == dat["implementation"]
                        ][0]
                        control_implementations_to_update.append(dat)
            except requests.RequestException as rex:
                logger.error(rex)
            except IndexError as iex:
                logger.error("Index Error: %s\n%s", dat, iex)
    logger.debug(control_implementations_to_insert)
    # Insert or update new control implementations
    if control_implementations_to_insert:
        api.update_server(
            method="post",
            url=config["domain"] + "/api/controlImplementation",
            message=f"Inserting {len(control_implementations_to_insert)} implementations..",
            json_list=control_implementations_to_insert,
        )
    if control_implementations_to_update:

        api.update_server(
            method="put",
            url=config["domain"] + "/api/controlImplementation",
            message=f"Updating {len(control_implementations_to_update)} implementations..",
            json_list=control_implementations_to_update,
        )


def process_component(file_name: str) -> None:
    """OSCAL Component to RegScale

    Args:
        file_name (str): Enter File Name
    """
    output_name = tempfile.gettempdir() + sep + "component.json"
    logger.debug(file_name)
    file_convert_json(file_name, output_name)
    try:
        json_d = open(output_name, "r").read()
    except FileNotFoundError:
        logger.error("File not found!\n%s", output_name)
        sys.exit(1)
    convert_oscal_comp_to_regscale(j_data=json.loads(json_d))
    remove(output_name)


def file_convert_json(input: str, output: str) -> None:
    """
    Convert file from YML/XML to JSON
    """
    # Create object

    with open(input, "r") as file_in, open(output, "w") as file_out:
        if Path(input).suffix == ".xml":
            obj = xmltodict.parse((file_in.read()))
        if Path(input).suffix in [".yaml", ".yml"]:
            obj = yaml.safe_load(file_in.read())
        json.dump(obj, file_out)


# Convert OSCAL formatted catalog json file to OSCAL xml
@oscal.command(name="convert")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.argument("command_type", type=click.STRING)
@click.argument("file_type", type=click.STRING)
def convert(input: str, output: str, command_type: str, file_type: str):
    """Convert any file type using oscal-cli tool

    Provide INPUT filename or path

    Provide OUTPUT filename or path

    Provide Command Type (catalog, profile, component-definition, ssp, mapping-collection, ap, ar, poam, metaschema)

    Provide OUTPUT Type: (xml, json, yaml)

    ex. regscale oscal convert /data/basic-ssp.json /tmp/output.xml ssp xml
    """
    oscal_convert(Path(input), Path(output), command_type, file_type)


def oscal_convert(input: Path, output: Path, command_type: str, file_type: str):
    """Call oscal-cli to perform conversion

    Args:
        input (Path): _description_
        output (Path): _description_
        command_type (str): _description_
        file_type (str): _description_
    """
    assert command_type.lower() in [
        "catalog",
        "profile",
        "component-definition",
        "ssp",
        "mapping-collection",
        "ap",
        "ar",
        "poam",
        "metaschema",
    ], "Please Enter a valid command type: (catalog, profile, component-definition, ssp, mapping-collection, ap, ar, poam, metaschema)"
    assert file_type.lower() in [
        "xml",
        "json",
        "yaml",
    ], "Please Enter a valid file type: (xml, json, or yaml)"
    logger.debug(Path(input))
    assert Path(input).exists()
    check_oscal()
    if "not found" not in app.get_java():
        if oscal_cli_path.exists():
            command = [
                oscal_cli_path,
                command_type,
                "convert",
                "--overwrite",
                "--to",
                file_type,
                input.absolute(),
                output.absolute(),
            ]
            logger.info(
                "Executing OSCAL Conversion... %s",
                [" ".join([str(item) for item in command])],
            )
            try:
                run(command, shell=False, check=True)
                logger.info("finished!  Output file saved: %s", output)
            except CalledProcessError as ex:
                if "status 3" not in str(ex):
                    logger.error("CalledProcessError: %s", ex)

    else:
        logger.warning(
            "Java distribution not found, Java is required to execute OSCAL conversion tools"
        )


# OSCAL Profile Loader Support
@oscal.command()
@click.option(
    "--title",
    prompt="Enter the title for the OSCAL profile",
    help="RegScale will name the profile with the title provided",
)
@click.option(
    "--categorization",
    prompt="Enter the FIPS categorization level",
    help="Choose from Low, Moderate, or High",
)
@click.option(
    "--catalog",
    prompt="Enter the RegScale Catalog ID to use",
    help="Primary key (unique ID) of the RegScale catalog",
)
@click.option(
    "--file_name",
    prompt="Enter the file name of the OSCAL profile to process",
    help="RegScale will process and load the profile along with all specified controls",
    type=click.Path(exists=True),
)
def profile(title, categorization, catalog, file_name):
    """OSCAL Profile Loader

    Args:
        title (str): Title
        categorization (str): Category information
        cat (str): Catalog Title
        file_name (str): Enter File Name
    """
    upload_profile(
        title=title, categorization=categorization, catalog=catalog, file_name=file_name
    )


# flake8: noqa: C901
def upload_profile(title, categorization, catalog, file_name):
    """OSCAL Profile Uploader

    Args:
        title (str): Title
        categorization (str): Category information
        cat (str): Catalog Title
        file_name (str): Enter File Name
    """
    # validation
    if file_name == "":
        logger.error("No file name provided.")
        sys.exit(1)
    elif title == "":
        logger.error("No title provided for this RegScale profile.")
        sys.exit(1)
    elif int(catalog) <= 0:
        logger.error("No catalog provided or catalog invalid.")
        sys.exit(1)
    elif (
        categorization != "Low"
        and categorization != "Moderate"
        and categorization != "High"
    ):
        logger.error("Categorization not provided or invalid.")
        sys.exit(1)
    else:
        # load the catalog
        try:
            oscal = open(file_name, "r", encoding="utf-8-sig")
            oscal_data = json.load(oscal)
        except Exception as ex:
            logger.debug(file_name)
            logger.error(
                "Unable to open the specified OSCAL file for processing.\n%s", ex
            )
            sys.exit(1)

        # load the config from YAML
        try:
            config = app.load_config()
        except FileNotFoundError:
            logger.error("Unable to open the init file.")
            sys.exit(1)

        # set headers
        str_user = config["userId"]
        headers = {"Accept": "application/json", "Authorization": config["token"]}

        # create a new profile
        profile = {
            "id": 0,
            "uuid": "",
            "name": title,
            "confidentiality": "",
            "integrity": "",
            "availability": "",
            "category": categorization,
            "profileOwnerId": str_user,
            "createdById": str_user,
            "dateCreated": None,
            "lastUpdatedById": str_user,
            "dateLastUpdated": None,
            "isPublic": True,
        }

        # create the profile
        url_prof = config["domain"] + "/api/profiles/"
        logger.info("RegScale creating a new profile....")
        try:
            prof_response = api.post(url=url_prof, headers=headers, json=profile)
            prof_json_response = prof_response.json()
            logger.info("\nProfile ID: " + str(prof_json_response["id"]))
            # get the profile ID
            int_profile = prof_json_response["id"]
        except requests.exceptions.RequestException as ex:
            logger.error("Unable to create profile in RegScale:\n%s", ex)
            sys.exit(1)

        # get the list of existing controls for the catalog
        url_sc = config["domain"] + "/api/SecurityControls/getList/" + str(catalog)
        try:
            sc_response = api.get(url_sc, headers=headers)
            sc_data = sc_response.json()
        except requests.exceptions.RequestException as ex:
            logger.error(
                "Unable to retrieve security controls for this catalog in RegScale: \n%s",
                ex,
            )
            sys.exit(1)

        # loop through each item in the OSCAL control set
        mappings = []
        for m in oscal_data["profile"]["imports"][0]["include-controls"][0]["with-ids"]:
            b_match = False
            for sc in sc_data:
                if m == sc["controlId"]:
                    b_match = True
                    map = {
                        "id": 0,
                        "profileID": int_profile,
                        "controlID": int(sc["id"]),
                    }
                    mappings.append(map)
                    break
            if b_match is False:
                logger.error("Unable to locate control: %s", m)

        # upload the controls to the profile as mappings
        url_maps = config["domain"] + "/api/profileMapping/batchCreate"
        try:
            api.post(url_maps, headers=headers, json=mappings)
            logger.info(
                "%s total mappings created in RegScale for this profile.",
                str(len(mappings)),
            )
        except requests.exceptions.RequestException as ex:
            logger.error(
                "Unable to create mappings for this profile in RegScale \n %s", ex
            )
            sys.exit(1)


# Process catalog from OSCAL
@oscal.command()
@click.option(
    "--file_name",
    prompt="Enter the file name of the NIST Catalog to process",
    help="RegScale will process and load the catalog along with all controls, statements, and parameters",
    type=click.Path(exists=True),
)
def catalog(file_name):
    """Process and load catalog to RegScale"""
    upload_catalog(file_name)


# flake8: noqa: C901
def upload_catalog(file_name):
    """Process and load catalog to RegScale"""
    # Create directory if not exists

    if not path.exists("processing"):
        mkdir("processing")
    # validation of file name
    if file_name == "":
        logger.error("No file name provided.")
        sys.exit(1)
    else:
        # load the catalog
        try:
            oscal_file_data = open(file_name, "r", encoding="utf-8-sig")
            oscalData = json.load(oscal_file_data)
        except requests.exceptions.RequestException as ex:
            logger.error(
                "Unable to open the specified OSCAL file for processing.\n%s", ex
            )
            sys.exit(1)

    # load the config from YAML
    try:
        config = app.load_config()
    except Exception:
        logger.error("Unable to open the init file.")
        sys.exit(1)

    # debug flag to pause upload when testing and debugging (always true for production CLI use)
    b_upload = True
    b_params = True
    b_tests = True
    b_objs = True
    b_deep_links = True

    # set headers
    str_user = config["userId"]
    headers = {"Accept": "application/json", "Authorization": config["token"]}

    # parse the OSCAL JSON to get related data (used to enrich base spreadsheet)
    catalog_arr = oscalData["catalog"]
    str_uuid = catalog_arr["uuid"]
    strResourceGUID = ""
    strResourceTitle = ""
    strCitation = ""
    strLinks = ""

    # process resources for lookup
    resources = []
    if "back-matter" in catalog_arr:
        back_matter_arr = catalog_arr["back-matter"]
        for i in back_matter_arr["resources"]:
            # make sure values exist
            if "title" in i:
                strResourceTitle = i["title"]
            if "uuid" in i:
                strResourceGUID = i["uuid"]
            if "citation" in i:
                citation = i["citation"]
                if "text" in citation:
                    strCitation = citation["text"]
            strLinks = ""
            if "rlinks" in i:
                links = i["rlinks"]
                for x in links:
                    if "href" in x:
                        strLinks += x["href"] + "<br/>"
            # add parsed/flattened resource to the array
            res = {
                "uuid": strResourceGUID,
                "short": strResourceTitle,
                "title": strCitation,
                "links": strLinks,
            }
            resources.append(res)

    # Write to file to visualize the output
    with open(f"processing{sep}resources.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(resources, indent=4))

    # create the resource table
    str_resources = ""
    str_resources += '<table border="1" style="width: 100%;"><tr style="font-weight: bold"><td>UUID</td><td>Title</td><td>Links</td></tr>'
    for res in resources:
        str_resources += "<tr>"
        str_resources += "<td>" + res["uuid"] + "</td>"
        str_resources += "<td>" + res["title"] + "</td>"
        str_resources += "<td>" + res["links"] + "</td>"
        str_resources += "</tr>"
    str_resources += "</table>"

    # set the catalog URL for your Atlasity instance
    url_cats = config["domain"] + "/api/catalogues/"

    # setup catalog data
    cat = {
        "title": catalog_arr["metadata"]["title"],
        "description": "This publication provides a catalog of security and privacy controls for information systems and organizations to protect organizational operations and assets, individuals, other organizations, and the Nation from a diverse set of threats and risks, including hostile attacks, human errors, natural disasters, structural failures, foreign intelligence entities, and privacy risks. <br/><br/><strong>Resources</strong><br/><br/>"
        + str_resources,
        "datePublished": catalog_arr["metadata"]["version"],
        "uuid": str_uuid,
        "lastRevisionDate": catalog_arr["metadata"]["version"],
        "url": "https://csrc.nist.gov/",
        "abstract": "This publication provides a catalog of security and privacy controls for federal information systems and organizations and a process for selecting controls to protect organizational operations (including mission, functions, image, and reputation), organizational assets, individuals, other organizations, and the Nation from a diverse set of threats including hostile cyber attacks, natural disasters, structural failures, and human errors (both intentional and unintentional). The security and privacy controls are customizable and implemented as part of an organization-wide process that manages information security and privacy risk. The controls address a diverse set of security and privacy requirements across the federal government and critical infrastructure, derived from legislation, Executive Orders, policies, directives, regulations, standards, and/or mission/business needs. The publication also describes how to develop specialized sets of controls, or overlays, tailored for specific types of missions/business functions, technologies, or environments of operation. Finally, the catalog of security controls addresses security from both a functionality perspective (the strength of security functions and mechanisms provided) and an assurance perspective (the measures of confidence in the implemented security capability). Addressing both security functionality and assurance helps to ensure that information technology component products and the information systems built from those products using sound system and security engineering principles are sufficiently trustworthy.",
        "keywords": "FIPS Publication 200; FISMA; Privacy Act; Risk Management Framework; security controls; FIPS Publication 199; security requirements; computer security; assurance;",
        "createdById": str_user,
        "lastUpdatedById": str_user,
    }

    # create the catalog and print success result
    if b_upload is True:
        logger.info("RegScale creating catalog....")
        try:
            logger.debug(f"url={url_cats}, headers={headers}, json={cat}")
            response = api.post(url=url_cats, headers=headers, json=cat)
            # response = requests.request(url=url_cats, headers=headers, json=cat)
            json_response = response.json()
            logger.info("Catalog ID: %s", str(json_response["id"]))
            # get the catalog ID
            intCat = json_response["id"]
        except requests.exceptions.RequestException as ex:
            logger.error(
                "Unable to create catalog in RegScale, try logging in again to pull a fresh token: \n%s",
                ex,
            )
            sys.exit(1)
    else:
        # don't set ID in debug mode
        intCat = 0

    # process NIST families of controls
    families = []
    oscal_controls = []
    parameters = []
    parts = []
    assessments = []

    # process groups of controls
    for i in catalog_arr["groups"]:
        str_family = i["title"]
        f = {
            "id": i["id"],
            "title": i["title"],
        }
        # add parsed item to the family array
        families.append(f)

        # loop through controls
        for ctrl in i["controls"]:

            # process the control
            new_ctrl = processControl(
                ctrl, resources, str_family, parameters, parts, assessments
            )
            oscal_controls.append(new_ctrl)

            # check for child controls/enhancements
            if "controls" in ctrl:
                child_ctrls = ctrl["controls"]
                for child_ctrl in child_ctrls:
                    child = processControl(
                        child_ctrl,
                        resources,
                        str_family,
                        parameters,
                        parts,
                        assessments,
                    )
                    oscal_controls.append(child)

    # # Write to file to visualize the output
    with open(f"processing{sep}families.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(families, indent=4))
    logger.info("%s total families processed.", str(len(families)))

    # # Write to file to visualize the output
    with open(f"processing{sep}controls.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(oscal_controls, indent=4))
    logger.info("%s total controls processed.", str(len(oscal_controls)))

    # # Write to file to visualize the output
    with open(f"processing{sep}parameters.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(parameters, indent=4))
    logger.info("%s total parameters processed.", str(len(parameters)))

    # # Write to file to visualize the output
    with open(f"processing{sep}parts.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(parts, indent=4))
    logger.info("%s total parts processed.", str(len(parts)))

    # # Write to file to visualize the output
    with open(f"processing{sep}tests.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(assessments, indent=4))
    logger.info("%s total assessments processed.", str(len(assessments)))

    # create controls array
    controls = []
    new_controls = []
    errors = []

    # create a counter for records created
    int_total = 0

    # RegScale URLs
    url_sc = config["domain"] + "/api/securitycontrols/"
    url_params = config["domain"] + "/api/controlParameters/"
    url_tests = config["domain"] + "/api/controlTestPlans/"
    url_objs = config["domain"] + "/api/controlObjectives/"

    # loop through and print the results
    for i in track(
        oscal_controls,
        description=f"Posting {len(oscal_controls):,} Security Controls to RegScale ..",
    ):

        # create each security control
        sc = {
            "title": i["id"] + " - " + i["title"],
            "controlType": "Stand-Alone",
            "controlId": i["id"],
            "description": i["parts"] + "<br/><br/>" + i["guidance"],
            "references": i["links"],
            "relatedControls": "",
            "subControls": "",
            "enhancements": i["enhancements"],
            "family": i["family"],
            "mappings": i["parameters"],
            "assessmentPlan": i["assessment"],
            "weight": 0,
            "practiceLevel": "",
            "catalogueID": intCat,
            "createdById": str_user,
            "lastUpdatedById": str_user,
        }

        # append the result
        controls.append(sc)

        # attempt to create the security control
        if b_upload is True:
            try:
                # upload to RegScale
                response = api.post(url=url_sc, headers=headers, json=sc)
                json_response = response.json()
                logger.debug("\n\nSuccess - " + sc["title"])
                int_total += 1

                # add the new controls
                new_controls.append(json_response)
            except requests.exceptions.RequestException:
                logger.error("Unable to create security control: " + sc["title"])
                errors.append(sc)

    # Write to file to visualize the output
    with open(f"processing{sep}mappedControls.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(controls, indent=4))

    # Write to file to visualize the output
    if b_upload is True:
        with open(f"processing{sep}newControls.json", "w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(new_controls, indent=4))
    else:
        load_controls = open(
            f"processing{sep}newControls.json", "r", encoding="utf-8-sig"
        )
        new_controls = json.load(load_controls)

    #############################################################################
    #
    #   Start Processing Child Records of the Controls
    #
    #############################################################################
    # only process if the controls exists to map to
    if len(new_controls) > 0:
        # load the parameters
        newParams = []
        for p in track(
            parameters,
            description=f"Posting {len(parameters):,} parameters to RegScale ..",
        ):
            # find the parent control
            ctrlLookup = next(
                (
                    item
                    for item in new_controls
                    if (item["controlId"] == p["controlId"])
                ),
                None,
            )
            if ctrlLookup is None:
                logger.error(
                    "Error: Unable to locate "
                    + p["controlId"]
                    + " for this parameter: "
                    + p["name"]
                )
            else:
                # create a new parameter to upload
                newParam = {
                    "id": 0,
                    "uuid": "",
                    "text": p["value"],
                    "dataType": "string",
                    "parameterId": p["name"],
                    "securityControlId": ctrlLookup["id"],
                    "archived": False,
                    "createdById": str_user,
                    "dateCreated": None,
                    "lastUpdatedById": str_user,
                    "dateLastUpdated": None,
                }

                # add the control to the new array
                newParams.append(newParam)

                # attempt to create the parameter
                if b_params is True:
                    try:
                        # upload to RegScale
                        response = api.post(url_params, headers=headers, json=newParam)
                        logger.debug(
                            "\n\nSuccess - "
                            + newParam["parameterId"]
                            + " parameter uploaded successfully."
                        )
                    except requests.exceptions.RequestException:
                        logger.error(
                            "Unable to create parameter: " + newParam["parameterId"]
                        )
                        errors.append(newParam)

        # output the result
        with open(
            f"processing{sep}newParameters.json", "w", encoding="utf-8"
        ) as outfile:
            outfile.write(json.dumps(newParams, indent=4))

        # load the tests
        newTests = []
        for ast in track(
            assessments,
            description=f"Posting {len(assessments):,} assessments to RegScale..",
        ):
            # find the parent control
            ctrlLookup = next(
                (
                    item
                    for item in new_controls
                    if (item["controlId"] == ast["parentControl"])
                ),
                None,
            )
            if ctrlLookup is None:
                logger.error(
                    "Error: Unable to locate "
                    + ast["parentControl"]
                    + " for this test: "
                )
            else:
                # create a new test to upload
                newTest = {
                    "id": 0,
                    "uuid": "",
                    "test": ast["testType"] + " - " + ast["description"],
                    "testId": str(uuid.uuid4()),
                    "securityControlId": ctrlLookup["id"],
                    "archived": False,
                    "createdById": str_user,
                    "dateCreated": None,
                    "lastUpdatedById": str_user,
                    "dateLastUpdated": None,
                }

                # add the test to the new array
                newTests.append(newTest)

                # attempt to create the test
                if b_tests is True:
                    try:
                        # upload to RegScale
                        response = api.post(url_tests, headers=headers, json=newTest)
                        json_response = response.json()
                        logger.debug(
                            "\n\nSuccess - "
                            + newTest["test"]
                            + " -  test uploaded successfully."
                        )
                    except requests.exceptions.RequestException:
                        logger.error("Unable to create test: " + newTest["test"])
                        errors.append(newTest)

        # output the result
        with open(f"processing{sep}newTests.json", "w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(newTests, indent=4))

        # load the objectives/parts
        newObjectives = []
        for p in track(
            parts, description=f"Posting {len(parts):,} objectives to RegScale.."
        ):
            # find the parent control
            ctrlLookup = next(
                (
                    item
                    for item in new_controls
                    if (item["controlId"] == p["parentControl"])
                ),
                None,
            )
            if ctrlLookup is None:
                logger.error(
                    "Error: Unable to locate "
                    + p["parentControl"]
                    + " for this objective/part: "
                    + p["name"]
                )
            else:
                # create a new test to upload
                newObj = {
                    "id": 0,
                    "uuid": "",
                    "name": p["name"],
                    "description": p["description"],
                    "objectiveType": p["objectiveType"],
                    "otherId": "",
                    "securityControlId": ctrlLookup["id"],
                    "parentObjectiveId": None,
                    "archived": False,
                    "createdById": str_user,
                    "dateCreated": None,
                    "lastUpdatedById": str_user,
                    "dateLastUpdated": None,
                }

                # add the part to the new array
                newObjectives.append(newObj)

                # attempt to create the objective
                if b_objs is True:
                    try:
                        # upload to RegScale
                        response = api.post(url_objs, headers=headers, json=newObj)
                        json_response = response.json()
                        logger.debug(
                            "\n\nSuccess - %s -  objective uploaded successfully.",
                            newObj["name"],
                        )
                    except requests.exceptions.RequestException as rex:
                        logger.error(
                            "Unable to create objective: %s\n%s", newObj["name"], rex
                        )
                        errors.append(newObj)

        # process deep links
        if b_deep_links is True:
            # get the list from RegScale
            try:
                logger.info(
                    "Retrieving all objectives for this catalogue # %i from RegScale (this might take a minute)...",
                    intCat,
                )
                url_deep = (
                    config["domain"]
                    + "/api/controlObjectives/getByCatalogue/"
                    + str(intCat)
                )
                objListResponse = api.get(url_deep, headers=headers)
                objList = objListResponse.json()
                logger.info(
                    "%i total objectives now retrieved from RegScale for processing.",
                    len(objList),
                )
            except Exception:
                logger.error(
                    "ERROR: Unable to retrieve control objective information from RegScale."
                )
                sys.exit(1)

            # loop through each objective and see if it has a parent, if so, update parent ID and send update to RegScale
            intUpdates = 0
            for objReg in track(
                objList, description=f"Updating {len(objList):,} objectives in RegScale"
            ):
                # find the part by name
                partLookup = next(
                    (item for item in parts if (item["name"] == objReg["name"])), None
                )
                if partLookup is not None:
                    # see if the part has a parent
                    if partLookup["parentObjective"] != "":
                        logger.debug("Found: " + partLookup["parentObjective"])
                        intUpdates += 1
                        # lookup the parent objective from RegScale
                        parentLookup = next(
                            (
                                item
                                for item in objList
                                if (item["name"] == partLookup["parentObjective"])
                            ),
                            None,
                        )
                        if parentLookup is not None:
                            logger.debug("Found Parent: " + parentLookup["name"])
                            # update the parent
                            updateParent = parentLookup["objective"]
                            updateParent["parentObjectiveId"] = parentLookup["id"]
                            try:
                                # upload to RegScale
                                api.put(
                                    str(url_objs) + str(updateParent["id"]),
                                    headers=headers,
                                    json=updateParent,
                                )
                                # updateData = updateResponse.json()
                                logger.debug(
                                    "Success - "
                                    + updateParent["name"]
                                    + " -  objective parent updated successfully."
                                )
                            except requests.exceptions.RequestException:
                                logger.error(
                                    "Unable to update parent objective: "
                                    + updateParent["name"]
                                )
                                errors.append(newObj)

            logger.info(str(intUpdates) + " total updates found.")

        # output the result
        with open(
            f"processing{sep}newObjectives.json", "w", encoding="utf-8"
        ) as outfile:
            outfile.write(json.dumps(newObjectives, indent=4))

        # output the errors
        with open(f"processing{sep}errors.json", "w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(errors, indent=4))


#############################################################################
#
#   Supporting Functions
#
#############################################################################

# function for recursively working through objectives
def processObjectives(obj, parts, ctrl, parent_id):
    """_summary_

    Args:
        obj (_type_): _description_
        parts (_type_): _description_
        ctrl (_type_): _description_
        parent_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    strOBJ = "<ul>"
    # loop through parts/objectives recursively
    for o in obj:
        # check prose
        strProse = ""
        if "prose" in o:
            strProse = o["prose"]

        # check name
        strName = ""
        if "name" in o:
            strName = o["name"]

        # create the new part
        part = {
            "id": 0,
            "name": o["id"],
            "objectiveType": strName,
            "description": strProse,
            "parentControl": ctrl["id"],
            "parentObjective": parent_id,
        }
        parts.append(part)
        strOBJ += "<li>{{" + o["id"] + "}}"
        if "prose" in o:
            strOBJ += " - " + strProse
        strOBJ += "</li>"
        if "parts" in o:
            strOBJ += processObjectives(o["parts"], parts, ctrl, o["id"])
    strOBJ += "</ul>"
    return strOBJ


# function to process each control
def processControl(ctrl, resources, str_family, parameters, parts, assessments):
    """_summary_

    Args:
        ctrl (_type_): _description_
        resources (_type_): _description_
        str_family (_type_): _description_
        parameters (_type_): _description_
        parts (_type_): _description_
        assessments (_type_): _description_

    Returns:
        _type_: _description_
    """
    # see if parameters exist
    if "params" in ctrl:
        # loop through each parameter
        for p in ctrl["params"]:
            # create a new parameter object
            pNew = {
                "name": p["id"],
                "value": "",
                "paramType": "",
                "controlId": ctrl["id"],
            }
            # process basic label
            if "label" in p:
                pNew["paramType"] = "text"
                pNew["value"] = p["label"]
            else:
                # initialize
                strParams = "Select ("
                # process select types
                if "select" in p:
                    select = p["select"]
                    if "how-many" in select:
                        strParams += select["how-many"]
                        pNew["paramType"] = "how-many"
                    if "choice" in select:
                        pNew["paramType"] = "choice"
                        strParams += "select) - "
                        for z in select["choice"]:
                            strParams += z + ", "
                    pNew["value"] = strParams
            # add to the array
            parameters.append(pNew)

    # get enhancements
    str_enhance = ""
    if "controls" in ctrl:
        childENHC = ctrl["controls"]
        str_enhance += "<strong>Enhancements</strong><br/><br/>"
        str_enhance += "<ul>"
        for che in childENHC:
            str_enhance += "<li>{{" + che["id"] + "}} - " + che["title"] + "</li>"
        str_enhance += "</ul>"

    # process control links
    int_link = 1
    str_links = ""
    if "links" in ctrl:
        for link in ctrl["links"]:
            # lookup the OSCAL control to enrich the data
            linkLookup = next(
                (item for item in resources if ("#" + item["uuid"]) == link["href"]),
                None,
            )
            if linkLookup is not None:
                str_links += (
                    str(int_link)
                    + ") "
                    + linkLookup["title"]
                    + " (OSCAL ID: "
                    + linkLookup["uuid"]
                    + ")<br/>"
                )
                int_link += 1
            else:
                str_links += link["href"] + "<br/>"

    # process parts
    part_info = ProcessParts(ctrl, parts, assessments)

    # add control
    new_ctrl = {
        "id": ctrl["id"],
        "title": ctrl["title"],
        "family": str_family,
        "links": str_links,
        "parameters": "",
        "parts": part_info["parts"],
        "assessment": part_info["assessments"],
        "guidance": part_info["guidance"],
        "enhancements": str_enhance,
    }

    # return the result
    return new_ctrl


def ProcessParts(ctrl, parts, assessments):
    """Process Parts

    Args:
        ctrl (list): _description_
        parts (list): _description_
        assessments (list): _description_

    Returns:
        str: _description_
    """
    # process parts
    if "parts" in ctrl:
        # initialize
        strParts = ""
        strGuidance = ""
        strAssessment = ""

        # create text field for human display
        strParts += "<ul>"
        for p in ctrl["parts"]:
            if ("id" in p) and (p["name"].startswith("assessment") is False):
                # check prose
                strProse = ""
                if "prose" in p:
                    strProse = p["prose"]

                # check name
                strName = ""
                if "name" in p:
                    strName = p["name"]

                # create the new part
                part = {
                    "id": 0,
                    "name": p["id"],
                    "objectiveType": strName,
                    "description": strProse,
                    "parentControl": ctrl["id"],
                    "parentObjective": "",
                }
                parts.append(part)
                # process objectives
                if (
                    p["name"] == "objective"
                    or p["name"] == "statement"
                    or p["name"] == "item"
                ):
                    try:
                        strParts += "<li>{{" + p["id"] + "}} - " + strProse + "</li>"
                    except Exception:
                        logger.error("Unable to parse part - " + str(p["id"]))
                    if "parts" in p:
                        strParts += processObjectives(p["parts"], parts, ctrl, p["id"])
                # process guidance
                if p["name"] == "guidance":
                    strGuidance = "<ul><li>Guidance</li>"
                    if "prose" in p:
                        strGuidance += "<ul>"
                        strGuidance += "<li>" + p["prose"] + "</li>"
                        strGuidance += "</ul>"
                    if "links" in p:
                        strGuidance += "<ul>"
                        for lkp in p["links"]:
                            strGuidance += (
                                "<li>" + lkp["href"] + ", " + lkp["rel"] + "</li>"
                            )
                        strGuidance += "</ul>"
                    strGuidance += "</ul>"
            else:
                # process assessments
                ProcessAssessments(p, ctrl, assessments)

        strParts += "</ul>"
    else:
        # no parts - set default values
        strParts = ""
        strGuidance = ""
        strAssessment = ""

    # return the result
    partInfo = {
        "parts": strParts,
        "guidance": strGuidance,
        "assessments": strAssessment,
    }
    return partInfo


# process assessment data
def ProcessAssessments(p, ctrl, assessments):
    # process assessments
    if p["name"].startswith("assessment") is True:
        # see if a lowe level objective that has prose
        if "prose" in p:
            # create new assessment objective
            ast = {
                "id": 0,
                "name": p["id"],
                "testType": p["name"],
                "description": p["prose"],
                "parentControl": ctrl["id"],
            }

            # see if it has any child tests
            if "parts" in p:
                if len(p["parts"]) > 0:
                    for item in p["parts"]:
                        ProcessAssessments(item, ctrl, assessments)
        else:
            # check the id
            strPartID = ""
            if "id" in p:
                strPartID = p["id"]
            else:
                strPartID = str(uuid.uuid4())

            # handle methods
            ast = {
                "id": 0,
                "name": strPartID,
                "testType": "",
                "description": "",
                "parentControl": ctrl["id"],
            }
            if "props" in p:
                if len(p["props"]) > 0:
                    if "value" in p["props"][0]:
                        ast["testType"] = p["props"][0]["value"]
            if "parts" in p:
                if len(p["parts"]) > 0:
                    if "prose" in p["parts"][0]:
                        ast["description"] = p["parts"][0]["prose"]

        # add test of the array
        if ast["description"] != "":
            assessments.append(ast)


def check_oscal():
    """Check if oscal dependencies are installed"""
    if (
        "unable to access jarfile".lower() in app.get_java()
        or not oscal_cli_path.exists()
    ):
        logger.error(
            "OSCAL CLI library not found, please check init.yaml and add the full cli path.  e.g. /opt/oscal-cli/bin/oscal-cli"
        )
        sys.exit(1)
