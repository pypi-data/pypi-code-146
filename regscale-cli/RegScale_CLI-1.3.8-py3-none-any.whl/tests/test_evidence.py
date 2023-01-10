#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""standard imports"""

import sys
from datetime import datetime
from app.api import Api
from app.application import Application
from app.logz import create_logger
from app.evidence import set_directory_variables
from app.evidence import parse_required_docs
from app.evidence import parse_required_texts
from app.evidence import document_assessment_results
from app.evidence import text_assessment_results
from app.evidence import gather_test_project_data
from app.evidence import create_child_assessments
from app.evidence import calculate_score_result
from app.evidence import text_string_search
from app.evidence import find_required_files_in_folder
from app.evidence import parse_required_text_from_files
from app.evidence import get_doc_timestamps
from app.evidence import remove
from app.evidence import delta
from app.evidence import assess_doc_timestamps


# Adds higher directory to python modules path.
sys.path.append("..")


class TestEvidence:
    """Tests for evidence.py"""

    # create logger function to log errors
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

    # test that thare are 3 variables returned as a tuple
    # that they are all with type of string
    # are not empty and contain specified keywords in directory names
    def test_set_directory_variables(self):
        """test directory variables"""
        variables = set_directory_variables()
        assert isinstance(variables, tuple[str, str, str])
        assert isinstance(variables[0], str)
        assert isinstance(variables[1], str)
        assert isinstance(variables[2], str)
        assert len(variables[0]) > 0
        assert len(variables[1]) > 0
        assert len(variables[2]) > 0

    # test that there are 3 variables returned as a tuple
    # that they are of type dict, list and list
    # that the number of required docs in list == number of dicts in list
    def test_parse_required_docs(self):
        """parse required documents"""
        docs = parse_required_docs()
        doclist = []
        for i in range(len(docs[0]["required-documents"])):
            item = docs[0]["required-documents"][i].get("file-name")
            doclist.append(item)
        assert isinstance(docs, tuple[dict, list[dict], list[str]])
        assert isinstance(docs[0], dict)
        assert isinstance(docs[1], list[dict])
        assert len(doclist) == len(docs[1])
        assert isinstance(docs[2], list[str])

    # test that 1 variable is returned as a list that is not empty
    def test_parse_required_texts(self):
        """parse required texts"""
        texts = parse_required_texts()
        assert isinstance(texts, list[str])
        assert len(texts) > 0

    # test that there is 1 variable returned as a bool
    def test_document_assessment_results(self):
        """test document assessment results"""
        results = document_assessment_results()
        assert isinstance(results, bool)

    # test that there is 1 variable returned as a bool
    def test_text_assessment_results(self):
        """test text assessment results"""
        results = text_assessment_results()
        assert isinstance(results, bool)

    # test that are 2 variables returned as a tuple
    # containing a non-empty list
    # a response status code integer with a value of 200
    def test_gather_test_project_data(self):
        """test the test project data"""
        data = gather_test_project_data()
        assert isinstance(data, tuple[list, int])
        assert isinstance(data[0], list)
        assert data[1] == 200

    # test that 1 variable is returned as a response status code integer with a value of 200
    def test_create_child_assessment(self):
        """test creation of child assessments"""
        create = create_child_assessments()
        assert isinstance(create, tuple[int, dict])
        assert isinstance(create[0], int)
        assert isinstance(create[1], dict)
        assert len(create[1]) > 0

    # test that 4 variables are returned as a tuple
    # containing a non-empty list of bools
    # with the other 3 variables being integers != 0
    def test_calculate_score_assessment(self):
        """test calculation of assessment score"""
        scores = calculate_score_result()
        assert isinstance(scores, tuple[list[bool], int, int, int])
        assert isinstance(scores[0], list[bool])
        assert len(scores[0]) > 0
        assert isinstance(scores[1], int)
        assert scores[1] > 0
        assert isinstance(scores[2], int)
        assert scores[2] > 0
        assert isinstance(scores[3], int)
        assert scores[3] > 0

    # test that 1 variable is returned as a list
    # containing a list of bools
    # that length of list = length of required texts
    def test_string_search(self):
        """test searching of strings for keywords"""
        searches = text_string_search()
        texts = parse_required_texts()
        assert isinstance(searches, list[bool])
        assert len(searches) == len(texts)

    # test that 2 variables are returned as a tuple
    # containing 2 lists of strings
    # that each list is not empty
    def test_find_required_files_in_folder(self):
        """test finding required files in folders"""
        required = find_required_files_in_folder()
        assert isinstance(required, tuple[str, str])
        assert isinstance(required[0], str)
        assert isinstance(required[1], str)
        assert len(required[0]) > 0
        assert len(required[1]) > 0

    # test that 1 variable is retuned as a list
    # containg strings
    # that the list is not empty
    def test_parse_required_texts_from_files(self):
        """test parsing required tests from files"""
        parsed = parse_required_text_from_files()
        assert isinstance(parsed, list[str])
        assert len(parsed) > 0

    # test that 1 variable is returned as a list
    # containing a dict that is not empty
    def test_get_doc_timestamps(self):
        """test retrieval of document timestamps"""
        timestamps = get_doc_timestamps()
        assert isinstance(timestamps, list[dict])
        for i in range(len(timestamps)):
            assert isinstance(timestamps[i]["last-modified"], int)
            assert isinstance(timestamps[i]["program"], str)
            assert isinstance(timestamps[i]["file"], str)
        assert len(timestamps) > 0

    # test that variable returned is at least 1 length
    # shorter then variable input into function
    # test that variable returned is a list of strings
    def test_remove(self):
        """tests remove function output"""
        letter_list = ["a", "b", "."]
        length = len(letter_list)
        assert length == 2
        remove(letter_list)
        new_length = len(letter_list)
        assert new_length < length
        assert isinstance(letter_list, list[str])

    # test that variable return is an int
    # that the conversion of float to datetime works
    # that the function accurately subtracts datetimes
    def test_delta(self):
        """tests delta function output"""
        float_num = 507482179.234
        date_num = datetime.fromtimestamp(float_num)
        assert isinstance(float_num, float)
        assert isinstance(date_num, datetime)
        days = delta(date_num)
        assert isinstance(days, int)

    # test that 1 variable is returned as a list of dicts
    # containing a dict that is not empty
    # with timestamp test result values
    def test_assess_doc_timestamps(self):
        """tests timestamp document assessment"""
        docs = parse_required_docs()
        required = docs[1]
        times = assess_doc_timestamps(required)
        assert isinstance(times, list[dict])
        for i in range(len(times)):
            assert isinstance(times[i]["program"], str)
            assert isinstance(times[i]["file-name"], str)
            assert isinstance(times[i]["test-results"], bool)
        assert len(times) > 0
