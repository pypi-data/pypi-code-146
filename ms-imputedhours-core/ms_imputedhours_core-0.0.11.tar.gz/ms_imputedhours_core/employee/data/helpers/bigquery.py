import os
from datetime import datetime


BIGQUERY_EMPLOYEE_CAPACITY = os.getenv('BIGQUERY_EMPLOYEE_CAPACITY_TABLE', 'ms--tiber-happeo--pro--aa82.jiradataintegration.employeecapacity')
class BigqueryUpdateQueryBuilder(object):
    def __init__(self, email, year, month, jira, fte, office, capacity, hiring_date, enddate, realcapacity):
        self.today = datetime.today()

        self.email = email
        self.year = year
        self.month = month
        self.jira = jira
        self.fte = fte
        self.office = office
        self.capacity = capacity
        self.hiring_date = hiring_date
        self.enddate = enddate
        self.realcapacity = realcapacity

    def _set_enddate_for_update(self):
        if self.enddate:
            return ", enddate='{}'".format(self.enddate)
        else:
            return ''

    def _set_startdate_for_update(self):
        if self.hiring_date:
            return ", startdate='{}'".format(self.hiring_date)
        else:
            return ''

    def build_update(self):
        return """
            UPDATE `{BIGQUERY_EMPLOYEE_CAPACITY}` SET
                email='{email}',
                month='{month}',
                year='{year}',
                fte={fte},
                office='{office}',
                jira={jira},
                capacity={capacity},
                realcapacity={realcapacity}
                {hiring_date}
                {enddate}
            WHERE
                email='{email}' AND
                month='{month}' AND
                year='{year}'
        """.format(
            email=self.email,
            year=self.year,
            month=self.month,
            jira=self.jira,
            fte=self.fte,
            office=self.office,
            capacity=self.capacity,
            hiring_date=self._set_startdate_for_update(),
            realcapacity=self.realcapacity,
            enddate=self._set_enddate_for_update(),
            BIGQUERY_EMPLOYEE_CAPACITY=BIGQUERY_EMPLOYEE_CAPACITY
        )

    def _get_insert_columns(self):
        basic_columns = 'email, month, year, fte, office, jira, capacity, realcapacity'

        if self.hiring_date:
            basic_columns += ', startdate'

        if self.enddate:
            basic_columns += ', enddate'
            

        return basic_columns

    def _set_enddate_insert(self):
        if self.enddate:
            return ",'{}'".format(self.enddate)
        return ''

    def _set_startdate_insert(self):
        if self.hiring_date:
            return ",'{}'".format(self.hiring_date)
        return ''

    def build_insert(self):
        return """
            INSERT INTO `{BIGQUERY_EMPLOYEE_CAPACITY}` ({columns}) VALUES (
                '{email}',
                '{month}',
                '{year}',
                {fte},
                '{office}',
                {jira},
                {capacity},
                {realcapacity}
                {hiring_date}
                {enddate}
            )
        """.format(
            columns=self._get_insert_columns(),
            email=self.email,
            year=self.year,
            month=self.month,
            jira=self.jira,
            fte=self.fte,
            office=self.office,
            capacity=self.capacity,
            realcapacity=self.realcapacity,
            hiring_date=self._set_startdate_insert(),
            enddate=self._set_enddate_insert(),
            BIGQUERY_EMPLOYEE_CAPACITY=BIGQUERY_EMPLOYEE_CAPACITY,
        )
