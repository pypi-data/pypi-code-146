#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Standard Imports """
import fnmatch
import json
import os
import sys
from datetime import datetime

import click  # type: ignore
import fitz  # type: ignore
import pandas as pd  # type: ignore
import pdfplumber  # type: ignore
from docx import Document  # type: ignore
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

from app.api import Api
from app.application import Application
from app.logz import create_logger


@click.group()
def evidence():
    """Starts the evidence collection automation process"""


@evidence.command()
def start():
    """Calls the collection process"""
    collection()


# flake8: noqa
def collection():
    """Wraps the logic of the evidence collection automation process"""

    # create logger function to log to the console
    logger = create_logger()

    # set environment and application configuration
    app = Application()
    api = Api(app)
    config = {}
    try:
        # load the config from YAML
        config = app.load_config()
    except FileNotFoundError:
        logger.error("ERROR: No init.yaml file or permission error when opening file.")

    def remove(list_to_review: list) -> None:
        """remove items that start with ."""
        # loop through folder/file list
        for item in list_to_review:
            # if the folder or file starts with '.'
            if item.startswith("."):
                # remove the item from the list
                list_to_review.remove(item)

    def delta(time: datetime) -> int:
        """calculates the days between 2 datetimes"""
        # find time difference between dates
        diff = datetime.now() - time
        # return the difference in integer days
        return diff.days

    def calc_score(number: int) -> int:
        """calculate score"""
        # bring in score lists
        true_scores = score_data[0]
        total_scores = score_data[2]
        # set score values
        true_score = true_scores[number]
        total_score = total_scores[number]
        # calculate test score for this result and check for zero division
        test_score = (
            int((true_score / total_score) * 100) if int(total_score) != 0 else 0
        )
        # return variable for use outside of local scope
        return test_score

    def find_signatures(file: str) -> int:
        """determine if the file is digitally signed"""
        # if the file is a pdf document
        if file.endswith(".pdf"):
            # open the document
            doc = fitz.open(file)
            # determine if document is digitally signed
            number = doc.get_sigflags()
            # if the sig flag is equal to 3
            if number == 3:
                logger.info(
                    "%s has signature fields and has been digitally signed", file
                )
            # if the sig flag is equal to 1
            elif number == 1:
                logger.info(
                    "%s has signature fields, but has not been digitally signed", file
                )
            # if the sig flag is equal to -1
            elif number == -1:
                logger.info(
                    "%s has no signature fields to hold a digital signature", file
                )
        # if the file is a docx document
        if file.endswith(".docx"):
            # set sig flag equal to 0
            number = 0
            logger.info("%s is not a pdf document", file)

        # return variable for use outside of local scope
        return number

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
    ) as progress:

        task0 = progress.add_task(
            "[white]Setting evidence folder directory variables", total=3
        )

        def set_directory_variables() -> tuple[str, str, str]:
            """set evidence folder directory variables"""
            # change working directory for evidence full path
            evidence_folder = app.config["evidenceFolder"]
            if evidence_folder is None or len(os.listdir(evidence_folder)) <= 1:
                sys.exit(
                    "The directory set to evidenceFolder cannot be found or is empty."
                )
            else:
                os.chdir(evidence_folder)
            progress.update(task0, advance=1)
            # include RegScale projects folder
            dir_name = [
                filename
                for filename in os.listdir(os.getcwd())
                if os.path.isdir(os.path.join(os.getcwd(), filename))
            ][0]
            progress.update(task0, advance=1)
            # pick up subdirectory under the evidence folder
            new_cwd = os.getcwd() + os.sep + dir_name
            progress.update(task0, advance=1)
            # return variables for use outside local scope
            return evidence_folder, dir_name, new_cwd

        # call function to define variable for use outside of function
        directories = set_directory_variables()

        task1 = progress.add_task(
            "[white]Building a required documents list from config.json", total=3
        )

        def parse_required_docs(evidence_folder: str) -> tuple[list[dict], set[str]]:
            """build a list of the required documents from config.json"""
            # create an empty list to hold a list of all document requirements for the assessment
            required_docs = []
            progress.update(task1, advance=1)
            # create an empty list to hold a list of all required documents
            document_list = set()
            progress.update(task1, advance=1)
            # open app//evidence//config.json file and read contents
            with open(
                evidence_folder + os.sep + "config.json", "r", encoding="utf-8"
            ) as json_file:
                # load json object into a readable dictionary
                rules = json.load(json_file)
                progress.update(task1, advance=1)
                # loop through required document dicts
                for i in range(len(rules["required-documents"])):
                    # add to a list of dictionaries for parsing
                    required_docs.append(
                        {
                            "file-name": rules["required-documents"][i].get(
                                "file-name"
                            ),
                            "last-updated-by": rules["required-documents"][i].get(
                                "last-updated-by"
                            ),
                            "signatures-required": rules["required-documents"][i].get(
                                "signatures-required"
                            ),
                            "signature-count": rules["required-documents"][i].get(
                                "signature-count"
                            ),
                        }
                    )
                    # update contents of list if it does not already exists
                    document_list.add(rules["required-documents"][i].get("file-name"))
            progress.update(task1, advance=1)
            # return variables for use outside of local scope
            return required_docs, document_list

        # call function to define variable for use outside of function
        docs = parse_required_docs(evidence_folder=directories[0])

        task2 = progress.add_task(
            "[white]Calculating files last modified times", total=5
        )

        def get_doc_timestamps(evidence_folder: str, directory: str) -> list[dict]:
            """get each file's last modified time"""
            # create empty list to hold file modified times
            modified_times: list[dict]
            modified_times = []
            progress.update(task2, advance=1)
            # get list of folders in parent folder
            folders_list = os.listdir(evidence_folder)
            progress.update(task2, advance=1)
            # remove any child folders that start with '.'
            remove(folders_list)
            progress.update(task2, advance=1)
            # loop through directory listing
            for folder in folders_list:
                # get list of files in each folder
                filelist = os.listdir(os.path.join(evidence_folder, folder))
                # remove any files that start with '.'
                remove(filelist)
                # loop through list of files in each folder
                for filename in filelist:
                    # append the modified time for each file to the list
                    modified_times.append(
                        {
                            "program": folder,
                            "file": filename,
                            "last-modified": os.path.getmtime(
                                os.path.join(directory, folder, filename)
                            ),
                        }
                    )
            progress.update(task2, advance=1)
            # loop through the list of timestamps
            for i, time_data in enumerate(modified_times):
                # update the last-modified value to be the count of days
                modified_times[i].update(
                    {
                        "last-modified": delta(
                            datetime.fromtimestamp(time_data["last-modified"])
                        )
                    }
                )
            progress.update(task2, advance=1)
            # return variable for use outside local scope
            return modified_times

        # call function to define variable for use outside of function
        times = get_doc_timestamps(
            evidence_folder=directories[2], directory=directories[1]
        )

        task3 = progress.add_task(
            "[white]Building a required texts list from config.json", total=3
        )

        def set_required_texts(evidence_folder: str) -> set[str]:
            """parse config.json file and build a list of the required texts for the assessment"""
            # create an empty set to hold all unique required texts for the assessment
            required_text = set()
            progress.update(task3, advance=1)
            # open app//evidence//config.json file and read contents
            with open(
                evidence_folder + os.sep + "config.json", "r", encoding="utf-8"
            ) as json_file:
                # load json object into a readable dictionary
                rules = json.load(json_file)
                progress.update(task3, advance=1)
                # create iterator to traverse dictionary
                for i in range(len(rules["rules-engine"])):
                    # pull out required text to look for from config
                    for items in rules["rules-engine"][i]["text-to-find"]:
                        # exclude duplicate text to search from required text
                        required_text.add(items)
                progress.update(task3, advance=1)
            # return variable for use outside of local scope
            return required_text

        # call function to define variable for use outside of function
        texts = set_required_texts(evidence_folder=directories[0])

        task4 = progress.add_task(
            "[white]Searching evidence folder for required files", total=4
        )

        def find_required_files_in_folder(evidence_folder: str) -> list[dict]:
            """pull out required files from each directory for parsing"""
            # create empty list to hold list of files in directory
            dir_list: list[dict]
            dir_list = []
            progress.update(task4, advance=1)
            # build a list of all folders to iterate through
            folder_list = os.listdir(evidence_folder)
            progress.update(task4, advance=1)
            # remove any folders starting with '.' from list
            remove(folder_list)
            progress.update(task4, advance=1)
            for folder in folder_list:
                # build a list of all files contained in sub-directories
                filelist = os.listdir(evidence_folder + os.sep + folder)
                # remove folders and file names that start with a .
                remove(filelist)
                for filename in filelist:
                    dir_list.append({"program": folder, "file": filename})
            progress.update(task4, advance=1)
            # return variable for use outside of local scope
            return dir_list

        # call function to define variable for use outside of function
        folders = find_required_files_in_folder(evidence_folder=directories[2])

        task5 = progress.add_task(
            "[white]Searching for digital signatures in documents", total=2
        )

        def signature_assessment_results(
            directory: list[dict], r_docs: list[dict]
        ) -> list[dict]:
            """compares signature config parameter against signature detection"""
            # create empty list to hold assessment results
            sig_assessments: list[dict]
            sig_assessments = []
            progress.update(task5, advance=1)
            # loop through list of found documents in each sub-folder
            for doc_file in directory:
                for required in r_docs:
                    if doc_file["file"] == required["file-name"]:
                        # if the signatures-required field is set to true
                        if required["signatures-required"] is True:
                            # run the signature detection function for the file
                            sig_result = find_signatures(doc_file["file"])
                            # if the return value is 3 pass the test
                            if sig_result == 3:
                                # append a true result for each document tested
                                sig_assessments.append(
                                    {
                                        "program": doc_file["program"],
                                        "file": doc_file["file"],
                                        "test": "signature-required",
                                        "result": True,
                                    }
                                )
                            # if the return value is 1, -1 or 0 fail the test
                            else:
                                # append a false result for each document tested
                                sig_assessments.append(
                                    {
                                        "program": doc_file["program"],
                                        "file": doc_file["file"],
                                        "test": "signature-required",
                                        "result": False,
                                    }
                                )
                        # if the signatures-required field is set to false
                        if required["signatures-required"] is False:
                            # append a true result for each document not requiring a signature
                            sig_assessments.append(
                                {
                                    "program": doc_file["program"],
                                    "file": doc_file["file"],
                                    "test": "signature-required (not required)",
                                    "result": True,
                                }
                            )
            progress.update(task5, advance=1)
            # return variable for use outside of local scope
            return sig_assessments

        # call function to define variable for use outside of function
        SIGRESULTS = signature_assessment_results(directory=folders, r_docs=docs[0])

        task6 = progress.add_task(
            "[white]Testing if required documents are present", total=2
        )

        def document_assessment_results(
            directory: list[dict], documents: set[str]
        ) -> list[dict]:
            """test if required documents are present in each directory"""
            # create empty list to hold assessment results
            doc_assessments: list[dict]
            doc_assessments = []
            progress.update(task6, advance=1)
            # loop through list of found documents in each sub-folder
            for doc_file in directory:
                # if the file in the sub-folder is in the required documents list
                if doc_file["file"] in documents:
                    # append a true result for each file in each program
                    doc_assessments.append(
                        {
                            "program": doc_file["program"],
                            "file": doc_file["file"],
                            "test": "required-documents",
                            "result": True,
                        }
                    )
                else:
                    # append a false result for each file in each program
                    doc_assessments.append(
                        {
                            "program": doc_file["program"],
                            "file": doc_file["file"],
                            "test": "required-documents",
                            "result": False,
                        }
                    )
            progress.update(task6, advance=1)
            # return variable for use outside of local scope
            return doc_assessments

        # call function to define variable for use outside of function
        DOCRESULTS = document_assessment_results(directory=folders, documents=docs[1])

        task7 = progress.add_task(
            "[white]Extracting texts from required files", total=4
        )

        def parse_required_text_from_files(evidence_folder: str) -> list[dict]:
            """parse text from docx/pdf file and hold strings representing required text to test"""
            # create an empty list to hold all strings from parsed documents
            full_text: list[dict]
            full_text = []
            progress.update(task7, advance=1)
            # build a list of files in the folder
            folder_list = os.listdir(evidence_folder)
            progress.update(task7, advance=1)
            # remove all folders that start with '.'
            remove(folder_list)
            progress.update(task7, advance=1)
            for folder in folder_list:
                # create a list of files to iterate through for parsing
                file_list = os.listdir((os.path.join(evidence_folder, folder)))
                remove(file_list)
                # iterate through all of the files in the list
                for filename in file_list:
                    # if the filename is a .docx file
                    if filename.endswith(".docx"):
                        # create empty overwritable list to hold text per file
                        output: list[str]
                        output = []
                        # open the word document to enable parsing
                        document = Document(
                            os.path.join(evidence_folder, folder, filename)
                        )
                        # iterate through each paragraph in the document
                        for para in document.paragraphs:
                            # append each paragraph of strings to the list
                            output.append(para.text)
                        # add each file and the requisite text to the dictionary to test
                        full_text.append(
                            {"program": folder, "file": filename, "text": output}
                        )
                    # if the filename is a .pdf file
                    elif filename.endswith(".pdf"):
                        # create empty overwritable list to hold text per file
                        output_text_list: list[str]
                        output_text_list = []
                        # open filename with pdfplumber
                        with pdfplumber.open(filename) as pdf:
                            # set number of pages
                            pages = pdf.pages
                            # for each page in the pdf document
                            for page in pages:
                                # extract the text
                                text = page.extract_text()
                                # write the text to a list
                                output_text_list.append(text)
                            # add each file and the requisite text to the dictionary to test
                            full_text.append(
                                {
                                    "program": folder,
                                    "file": filename,
                                    "text": output_text_list,
                                }
                            )
            progress.update(task7, advance=1)
            # return variable for use outside of local scope
            return full_text

        # call function to define variable for use outside of function
        file_texts = parse_required_text_from_files(evidence_folder=directories[2])

        task8 = progress.add_task(
            "[white]Searching for required text in parsed documents", total=2
        )

        def text_string_search(f_texts: list[dict], req_texts: set[str]) -> list[dict]:
            """search for required texts in document paragraphs"""
            # create empty list to hold assessment results
            search_list: list[dict]
            search_list = []
            progress.update(task8, advance=1)
            # iterate through each sentence in the required texts
            for parsed_file in f_texts:
                # then iterate through each parsed paragraph
                for line in req_texts:
                    # if the required text appears in the parsed paragraph
                    if any(line in text for text in parsed_file["text"]) is True:
                        # then create a "True" entry in the empty list
                        search_list.append(
                            {
                                "program": parsed_file["program"],
                                "file": parsed_file["file"],
                                "text": line,
                                "result": True,
                            }
                        )
                    else:
                        # else create a "False" entry in the empty list
                        search_list.append(
                            {
                                "program": parsed_file["program"],
                                "file": parsed_file["file"],
                                "text": line,
                                "result": False,
                            }
                        )
            progress.update(task8, advance=1)
            # return variable for use outside of local scope
            return search_list

        # call function to define variable for use outside of function
        search_results = text_string_search(f_texts=file_texts, req_texts=texts)

        task9 = progress.add_task(
            "[white]Testing if required texts are present", total=2
        )

        def text_assessment_results(
            searches: list[dict], r_texts: set[str]
        ) -> list[dict]:
            """test if required text is present in required files and return test assessment"""
            # create empty list to hold assessment results
            text_results: list[dict]
            text_results = []
            progress.update(task9, advance=1)
            # loop through text string search results
            for result in searches:
                # loop through required texts
                for line in r_texts:
                    # if the text matches the required text
                    if result["text"] == line:
                        text_info = result["text"]
                        # if the result of the previous text search was true
                        if result["result"] is True:
                            # condense results into 1 per file
                            text_results.append(
                                {
                                    "program": result["program"],
                                    "file": result["file"],
                                    "test": f"required-text ({text_info})",
                                    "result": result["result"],
                                }
                            )
            # return variable for use outside of local scope
            progress.update(task9, advance=1)
            # return variable for use outside of local scope
            return text_results

        # call function to define variable for use outside of function
        TEXTRESULTS = text_assessment_results(searches=search_results, r_texts=texts)

        task10 = progress.add_task(
            "[white]Retrieving data from the evidence test projects", total=3
        )

        def gather_test_project_data(evidence_folder: str) -> list[dict]:
            """gather information from evidence test projects created in RegScale to catch data"""
            # create empty list to hold project test data from GET API call
            test_data: list[dict]
            test_data = []
            progress.update(task10, advance=1)
            # test project information created in Regscale UI
            with open(
                evidence_folder + os.sep + "list.json", "r", encoding="utf-8"
            ) as json_file:
                # load json object into a readable dictionary
                lists = json.load(json_file)
                # loop through projects in the list.json
                for i in range(len(lists["parser-list"])):
                    # append the id and program to the list of test projects
                    test_data.append(
                        {
                            "id": lists["parser-list"][i].get("id"),
                            "program": lists["parser-list"][i].get("folder-name"),
                        }
                    )
            progress.update(task10, advance=1)
            # create empty list to hold json response data for each project
            test_info: list[dict]
            test_info = []
            # iterate through test projects and make sequential GET API calls
            for item in test_data:
                # make a GET request for each project
                response = api.get(
                    url=f'{app.config["domain"]}/api/projects/{item["id"]}',
                    headers={
                        "Accept": "application/json",
                        "Authorization": config["token"],
                    },
                )
                if response.status_code == 200:
                    logger.info("Project data retrieval was successful")
                else:
                    logger.info("Project data retrieval was unsuccessful")
                # save the json response data
                json_data = response.json()
                test_info.append(
                    {
                        "id": json_data["id"],
                        "title": json_data["title"],
                        "uuid": json_data["uuid"],
                        "projectmanagerid": json_data["projectManagerId"],
                        "parentid": json_data["parentId"],
                        "parentmodule": json_data["parentModule"],
                        "program": item["program"],
                    }
                )
            progress.update(task10, advance=1)
            # return variables for use outside of local scope
            return test_info

        # call function to define variable for use outside of function
        data = gather_test_project_data(evidence_folder=directories[0])

        task11 = progress.add_task("[white]Testing file modification times", total=2)

        def assess_doc_timestamps(
            timestamps: list[dict], documents: list[dict]
        ) -> list[dict]:
            """test file modification times"""
            # create empty list to store test results
            assessed_timestamps = []
            progress.update(task11, advance=1)
            # loop through timestamps
            for items in timestamps:
                # loop through required documents
                for doc_items in documents:
                    # if file names match between the list of dicts
                    if fnmatch.fnmatch(items["file"], doc_items["file-name"]):
                        # if the required modification time is less than the last modified days
                        if items["last-modified"] < doc_items["last-updated-by"]:
                            # append true result to the list of dicts
                            assessed_timestamps.append(
                                {
                                    "program": items["program"],
                                    "file": items["file"],
                                    "test": "last-updated-by",
                                    "result": True,
                                }
                            )
                        else:
                            # append false results to the list of dicts
                            assessed_timestamps.append(
                                {
                                    "program": items["program"],
                                    "file": items["file"],
                                    "test": "last-updated-by",
                                    "result": False,
                                }
                            )
            progress.update(task11, advance=1)
            # return variables for use outside of local scope
            return assessed_timestamps

        # call function to define variable to use outside of function
        TIMERESULTS = assess_doc_timestamps(timestamps=times, documents=docs[0])

        task12 = progress.add_task("[white]Building assessment report", total=4)

        def assessments_report(
            docres: list[dict],
            textres: list[dict],
            timeres: list[dict],
            sigres: list[dict],
        ) -> list[dict]:
            """this function builds the assessment report for all results"""
            # create a list to hold all of the assessment results
            assessment_report: list[dict]
            assessment_report = []
            progress.update(task12, advance=1)
            # append all results to 1 master list
            for result in docres:
                assessment_report.append(result)
            progress.update(task12, advance=1)
            # append all results to 1 master list
            for result in textres:
                assessment_report.append(result)
            progress.update(task12, advance=1)
            # append all results to 1 master list
            for result in timeres:
                assessment_report.append(result)
            progress.update(task12, advance=1)
            # append all results to 1 master list
            for result in sigres:
                assessment_report.append(result)
            progress.update(task12, advance=1)
            # return variable for use outside of local scope
            return assessment_report

        # call function to define variable to use outside of function
        report = assessments_report(
            docres=DOCRESULTS,
            textres=TEXTRESULTS,
            timeres=TIMERESULTS,
            sigres=SIGRESULTS,
        )

        task13 = progress.add_task(
            "[white]Building assessment results dataframe", total=4
        )

        def build_assessment_dataframe(assessments: list[dict]) -> list[dict]:
            """build dataframe for assessment results"""
            # build out dataframe for score calculations
            result_df = pd.DataFrame(assessments)
            progress.update(task13, advance=1)
            # fill in NaN cells
            result_df = result_df.fillna(" ")
            progress.update(task13, advance=1)
            # loop through the program column and split based on values
            dfs = [d for _, d in result_df.groupby("program")]
            # create an empty list to store dataframe results
            result_list: list[dict]
            result_list = []
            progress.update(task13, advance=1)
            # loop through dataframes
            for dfr in dfs:
                # pull out unique value counts for true
                true_counts = dfr["result"].value_counts()
                true_counts = dict(true_counts)
                # pull out unique value counts for false
                false_counts = dfr["result"].value_counts()
                false_counts = dict(false_counts)
                # create ints to hold count values
                pass_count: int
                fail_count: int
                pass_count = 0
                fail_count = 0
                # loop through true_counts list
                for i in true_counts:
                    # if value is true
                    if i is True:
                        # set equal to pass value
                        pass_count = true_counts[i]
                    if i is False:
                        # set equal to fail value
                        fail_count = false_counts[i]
                # output results to list of results
                result_list.append(
                    {
                        "program": dfr["program"].iloc[0],
                        "true": max(pass_count, 0),
                        "false": max(fail_count, 0),
                        "total": len(dfr),
                    }
                )
            progress.update(task13, advance=1)
            # return variable for use outside of local scope
            return result_list

        # call function to define variable to use outside of function
        results = build_assessment_dataframe(assessments=report)

        task14 = progress.add_task("[white]Calculating assessment score", total=1)

        def build_score_data(
            assessments: list[dict],
        ) -> tuple[list[int], list[int], list[int]]:
            """build assessment score lists"""
            # create empty lists to hold true/false counts
            true_list: list[int]
            true_list = []
            progress.update(task14, advance=1)
            false_list: list[int]
            false_list = []
            progress.update(task14, advance=1)
            total_list: list[int]
            total_list = []
            progress.update(task14, advance=1)
            # loop through assessment report data
            for item in assessments:
                # append true/false/total values to lists
                true_list.append(item["true"])
                false_list.append(item["false"])
                total_list.append(item["total"])
            progress.update(task14, advance=1)
            # return variable for use outside of local scope
            return true_list, false_list, total_list

        # call function to define variable for use outside of function
        score_data = build_score_data(assessments=results)

        task15 = progress.add_task(
            "[white]Building a table for the assessment report", total=4
        )

        def build_html_table(assessments: list[dict]) -> list[dict]:
            """this wil be a dictionary to html table conversion"""
            output_list: list[dict]
            output_list = []
            # create a dataframe of a list of dicts
            table_df = pd.DataFrame(data=assessments)
            progress.update(task15, advance=1)
            # fill in N/A cells with blank string
            table_df = table_df.fillna(" ")
            progress.update(task15, advance=1)
            # split dataframe into list of dataframes
            dfs = [d for _, d in table_df.groupby("program")]
            progress.update(task15, advance=1)
            # loop through dataframes
            for table_df in dfs:
                # output dataframe to an html table
                output = table_df.to_html()
                progress.update(task15, advance=1)
                # replace false values with inline styling conditional to red colors for False values
                output = output.replace(
                    "<td>False</td>", '<td style="color:red;">False</td>'
                )
                progress.update(task15, advance=1)
                # replace true values with inline styling conditional to green colors for True values
                output = output.replace(
                    "<td>True</td>", '<td style="color:green;">True</td>'
                )
                progress.update(task15, advance=1)
                # build list of outputs to loop through for API POST calls
                output_list.append(
                    {"program": table_df["program"].iloc[0], "html": output}
                )
            progress.update(task15, advance=1)
            # return variable for use outside of local scope
            return output_list

        # call function to define variable for use outsie of function
        html_output = build_html_table(assessments=report)

        task16 = progress.add_task(
            "[white]Creating child assessment based on test results", total=2
        )

        def create_child_assessments(
            project_data: list[dict], output: list[dict]
        ) -> None:
            """create assessments based on results of text parsing tests"""
            # set completion datetime to required format
            completion_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            progress.update(task16, advance=1)
            # loop through test projects and make an API call for each
            for i, project in enumerate(project_data):
                # call score calculation function
                test_score = calc_score(i)
                # if file name matches html output table program name
                if project_data[i]["program"] == output[i]["program"]:
                    # build assessment data
                    assessment_data = {
                        "leadAssessorId": app.config["userId"],
                        "title": "Evidence Collection Automation Assessment",
                        "assessmentType": "Inspection",
                        "status": "In Progress",
                        "projectId": project["id"],
                        "parentId": project["id"],
                        "parentModule": "projects",
                        "assessmentReport": output[i]["html"],
                        "assessmentPlan": "Review automated results of evidence collection tests",
                        "createdById": app.config["userId"],
                        "lastUpdatedById": app.config["userId"],
                        "complianceScore": test_score,
                        "isPublic": True,
                    }
                    # if all tests passed above score update POST call information
                    if test_score >= app.config["passScore"]:
                        # update assessment data API body information
                        assessment_data.update({"assessmentResult": "Pass"})
                        assessment_data["status"] = "Complete"
                        assessment_data.update({"actualFinish": completion_date})
                        assessment_data.update({"plannedStart": completion_date})
                        assessment_data.update({"plannedFinish": completion_date})
                        update_request = api.post(
                            f'{app.config["domain"]}/api/assessments',
                            json=assessment_data,
                        )
                        status_code = update_request.status_code
                    # if all tests failed below score update POST call information
                    elif test_score <= app.config["failScore"]:
                        # update assessment data API body information
                        assessment_data.update({"assessmentResult": "Fail"})
                        assessment_data["status"] = "Complete"
                        assessment_data.update({"actualFinish": completion_date})
                        assessment_data.update({"plannedStart": completion_date})
                        assessment_data.update({"plannedFinish": completion_date})
                        update_request = api.post(
                            f'{app.config["domain"]}/api/assessments',
                            json=assessment_data,
                        )
                        status_code = update_request.status_code
                        # if some tests passed in between score update POST call information
                    else:
                        # update assessment data API body information
                        assessment_data.update({"assessmentResult": "Partial Pass"})
                        assessment_data["status"] = "Complete"
                        assessment_data.update({"actualFinish": completion_date})
                        assessment_data.update({"plannedStart": completion_date})
                        assessment_data.update({"plannedFinish": completion_date})
                        update_request = api.post(
                            f'{app.config["domain"]}/api/assessments',
                            json=assessment_data,
                        )
                        status_code = update_request.status_code
                # log successful
                if status_code == 200:
                    logger.info("Child assessment creation was successful")
                else:
                    logger.info("Child assessment creation was not successful")
            progress.update(task16, advance=1)

        # call function to create child assessment via POST request
        create_child_assessments(project_data=data, output=html_output)
