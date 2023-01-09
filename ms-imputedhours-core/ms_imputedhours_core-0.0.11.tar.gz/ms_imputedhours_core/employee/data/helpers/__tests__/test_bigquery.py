import unittest
from unittest.mock import patch
from datetime import datetime

from ..bigquery import BigqueryUpdateQueryBuilder


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.email = 'test@test.com'
        self.year = 2022
        self.month = 1
        self.jira_hours = 40
        self.fte = 100
        self.office = 'Madrid'
        self.capacity = 80
        self.hiring_date = datetime.strptime(
            '02/01/22 00:00:00', '%m/%d/%y %H:%M:%S')
        self.enddate = None
        self.realcapacity = 80

        self.bigquery_builder = BigqueryUpdateQueryBuilder(
            email=self.email,
            year=self.year,
            month=self.month,
            jira=self.jira_hours,
            fte=self.fte,
            office=self.office,
            capacity=self.capacity,
            hiring_date=self.hiring_date,
            enddate=self.enddate,
            realcapacity=self.realcapacity,
        )

    def test_enddate_update_query_should_return_empty_string_when_enddate_is_None(self):
        expected_enddate_query = ''
        self.assertEqual(
            self.bigquery_builder._set_enddate_for_update(), expected_enddate_query)

    def test_hiring_date_update_query_should_return_date_query_when_hiring_date(self):
        expected_hiring_query = ", startdate='2022-02-01 00:00:00'"
        self.assertEqual(
            self.bigquery_builder._set_startdate_for_update(), expected_hiring_query)

    def test__set_startdate_insert_should_return_startdate_value(self):
        expected_hiring_query = ",'2022-02-01 00:00:00'"
        self.assertEqual(
            self.bigquery_builder._set_startdate_insert(), expected_hiring_query)

    def test__set_enddate_insert_should_return_enddate_value(self):
        expected_enddate_query = ""
        self.assertEqual(
            self.bigquery_builder._set_enddate_insert(), expected_enddate_query)

    def test_build_update_shouldd_return_update_capacity_table_query(self):
        expected_query = """
            UPDATE `ms--tiber-happeo--pro--aa82.jiradataintegration.employeecapacity` SET
                email='test@test.com',
                month='1',
                year='2022',
                fte=100,
                office='Madrid',
                jira=40,
                capacity=80,
                realcapacity=80
                , startdate='2022-02-01 00:00:00'
                
            WHERE
                email='test@test.com' AND
                month='1' AND
                year='2022'
        """

        self.assertMultiLineEqual(
            self.bigquery_builder.build_update(),
            expected_query,
        )

    def test_build_insert_shouldd_return_insert_capacity_table_query_without_enddate(self):
        expected_query = """
            INSERT INTO `ms--tiber-happeo--pro--aa82.jiradataintegration.employeecapacity` (email, month, year, fte, office, jira, capacity, realcapacity, startdate) VALUES (
                'test@test.com',
                '1',
                '2022',
                100,
                'Madrid',
                40,
                80,
                80
                ,'2022-02-01 00:00:00'
                
            )
        """

        self.assertMultiLineEqual(
            self.bigquery_builder.build_insert(),
            expected_query,
        )

    def test_build_insert_shouldd_return_insert_capacity_table_query_with_enddate(self):
        self.bigquery_builder = BigqueryUpdateQueryBuilder(
            email=self.email,
            year=self.year,
            month=self.month,
            jira=self.jira_hours,
            fte=self.fte,
            office=self.office,
            capacity=self.capacity,
            hiring_date=self.hiring_date,
            enddate=datetime.strptime('02/01/23 00:00:00', '%m/%d/%y %H:%M:%S'),
            realcapacity=self.realcapacity,
        )
        expected_query = """
            INSERT INTO `ms--tiber-happeo--pro--aa82.jiradataintegration.employeecapacity` (email, month, year, fte, office, jira, capacity, realcapacity, startdate, enddate) VALUES (
                'test@test.com',
                '1',
                '2022',
                100,
                'Madrid',
                40,
                80,
                80
                ,'2022-02-01 00:00:00'
                ,'2023-02-01 00:00:00'
            )
        """

        self.assertMultiLineEqual(
            self.bigquery_builder.build_insert(),
            expected_query,
        )

    def test_build_update_shouldd_return_update_capacity_table_query_with_enddate(self):
        self.bigquery_builder = BigqueryUpdateQueryBuilder(
            email=self.email,
            year=self.year,
            month=self.month,
            jira=self.jira_hours,
            fte=self.fte,
            office=self.office,
            capacity=self.capacity,
            hiring_date=self.hiring_date,
            enddate=datetime.strptime('02/01/23 00:00:00', '%m/%d/%y %H:%M:%S'),
            realcapacity=self.realcapacity,
        )
        expected_query = """
            INSERT INTO `ms--tiber-happeo--pro--aa82.jiradataintegration.employeecapacity` (email, month, year, fte, office, jira, capacity, realcapacity, startdate, enddate) VALUES (
                'test@test.com',
                '1',
                '2022',
                100,
                'Madrid',
                40,
                80,
                80
                ,'2022-02-01 00:00:00'
                ,'2023-02-01 00:00:00'
            )
        """

        self.assertMultiLineEqual(
            self.bigquery_builder.build_insert(),
            expected_query,
        )
