import os
from gc_google_services_api.bigquery import execute_query

from ms_imputedhours_core.employee.data.helpers.bigquery import BigqueryUpdateQueryBuilder
from ms_imputedhours_core.employee.data.helpers.dates import get_first_day, get_last_day

BIGQUERY_JIRA_DATA_TYPES = os.getenv(
    'BIGQUERY_JIRA_DATA_TYPES_TABLE', 'ms--tiber-happeo--pro--aa82.jiradataintegration.jiradatatypes')
BIGQUERY_SUCCESS_FACTOR = os.getenv(
    'BIGQUERY_SUCCESS_FACTOR_TABLE', 'ms--tiber-happeo--pro--aa82.jiradataintegration.dataemployees')
BIGQUERY_EMPLOYEE_CAPACITY = os.getenv(
    'BIGQUERY_EMPLOYEE_CAPACITY_TABLE', 'ms--tiber-happeo--pro--aa82.jiradataintegration.employeecapacity')

QUERY_HOURS_IMPUTED_OFFICE_EMPLOYEES = """
    SELECT
        *
    FROM
        `{BIGQUERY_JIRA_DATA_TYPES}`
    WHERE
        started >= "{from_date}" AND
        started <= "{to_date}" AND
        authorEmail IN ({emails})
"""

QUERY_HOURS_IMPUTED_ALL_EMPLOYEES = """
    SELECT
        *
    FROM
        `{BIGQUERY_JIRA_DATA_TYPES}`
    WHERE
        started >= "{from_date}" AND
        started <= "{to_date}"
"""

QUERY_HOURS_IMPUTED = """
    SELECT 
        *
    FROM 
        `{BIGQUERY_JIRA_DATA_TYPES}`
    WHERE
        started >= "{from_date}" AND
        started <= "{to_date}" AND
        authorEmail = "{email}"
"""

QUERY_SUCCESS_FACTOR = """
        SELECT
            * 
        FROM 
            `{BIGQUERY_SUCCESS_FACTOR}`
        WHERE
            email = "{email}"
    """

QUERY_SUCCESS_FACTOR_ALL = """
        SELECT
            * 
        FROM 
            `{BIGQUERY_SUCCESS_FACTOR}`
        WHERE
            office = '{office_name}'
    """

QUERY_SUCCESS_FACTOR_ALL_DATA = """
        SELECT
            * 
        FROM 
            `{BIGQUERY_SUCCESS_FACTOR}`
    """

QUERY_EMPLOYEE_CAPACITY = """
        SELECT
            * 
        FROM 
            `{BIGQUERY_EMPLOYEE_CAPACITY}`
        WHERE
            email = "{email}" AND
            month='{month}' AND
            year='{year}'
       
    """

QUERY_ALL_EMPLOYEE_CAPACITY = """
        SELECT
            * 
        FROM 
            `{BIGQUERY_EMPLOYEE_CAPACITY}`
        WHERE
            month='{month}' AND
            year='{year}'
       
    """

QUERY_REGISTER_EMPLOYEE_CAPACITY = """
    INSERT INTO `{BIGQUERY_EMPLOYEE_CAPACITY}` (email, month, year, fte, office, jira, capacity, startdate, enddate, realcapacity) VALUES (
        '{email}',
        '{month}',
        '{year}',
        {fte},
        '{office}',
        {jira},
        {capacity},
        '{hiring_date}',
        {enddate},
        {realcapacity}
    ) 
    """

QUERY_UPDATE_EMPLOYEE_CAPACITY = """
    UPDATE `{BIGQUERY_EMPLOYEE_CAPACITY}` SET
        email='{email}',
        month='{month}',
        year='{year}',
        fte={fte},
        office='{office}',
        jira={jira},
        capacity={capacity},
        startdate='{hiring_date}',
        enddate='{enddate}'
    WHERE
        email='{email}' AND
        month='{month}' AND
        year='{year}'
       
    """
MS_FOR_HOUR = 3600000


def get_all_data(date, office_emails):
    from_date = get_first_day(date).strftime("%Y-%m-%d")
    to_date = get_last_day(date).strftime("%Y-%m-%d")
    email_query_list = ",".join(["'{}'".format(email)
                                for email in office_emails])
    query = QUERY_HOURS_IMPUTED_OFFICE_EMPLOYEES.format(
        from_date=from_date,
        to_date=to_date,
        emails=email_query_list,
        BIGQUERY_JIRA_DATA_TYPES=BIGQUERY_JIRA_DATA_TYPES
    )

    return execute_query(query, error_value=[])


def get_imputed_hours(from_date, to_date):
    from_date = from_date.strftime("%Y-%m-%d")
    to_date = to_date.strftime("%Y-%m-%d")
    query = QUERY_HOURS_IMPUTED_ALL_EMPLOYEES.format(
        from_date=from_date,
        to_date=to_date,
        BIGQUERY_JIRA_DATA_TYPES=BIGQUERY_JIRA_DATA_TYPES
    )

    return execute_query(query, error_value=[])


def get_all_data_by_dates(from_date, to_date, office_emails):
    email_query_list = ",".join(["'{}'".format(email)
                                for email in office_emails])
    query = QUERY_HOURS_IMPUTED_OFFICE_EMPLOYEES.format(
        from_date=from_date,
        to_date=to_date,
        emails=email_query_list,
        BIGQUERY_JIRA_DATA_TYPES=BIGQUERY_JIRA_DATA_TYPES
    )

    return execute_query(query, error_value=[])


def get_data_from_email(email, date):
    from_date = get_first_day(date).strftime("%Y-%m-%d")
    to_date = get_last_day(date).strftime("%Y-%m-%d")
    query = QUERY_HOURS_IMPUTED.format(
        from_date=from_date,
        to_date=to_date,
        email=email,
        BIGQUERY_JIRA_DATA_TYPES=BIGQUERY_JIRA_DATA_TYPES)

    return execute_query(query, error_value=[])


def get_successfactor_data(email):
    query = QUERY_SUCCESS_FACTOR.format(
        email=email,
        BIGQUERY_SUCCESS_FACTOR=BIGQUERY_SUCCESS_FACTOR)

    return execute_query(query, error_value=[])


def get_successfactor_all_data(office_name):
    query = QUERY_SUCCESS_FACTOR_ALL.format(
        BIGQUERY_SUCCESS_FACTOR=BIGQUERY_SUCCESS_FACTOR,
        office_name=office_name
    )
    return execute_query(query, error_value=[])


def get_successfactor_all_offices():
    query = QUERY_SUCCESS_FACTOR_ALL_DATA.format(
        BIGQUERY_SUCCESS_FACTOR=BIGQUERY_SUCCESS_FACTOR
    )
    return execute_query(query, error_value=[])


def get_all_employee_capacity(month, year):
    query = QUERY_ALL_EMPLOYEE_CAPACITY.format(
        BIGQUERY_EMPLOYEE_CAPACITY=BIGQUERY_EMPLOYEE_CAPACITY,
        month=month,
        year=year,
    )
    return execute_query(query, error_value=[])


def get_employee_capacity(email, year, month):
    query = QUERY_EMPLOYEE_CAPACITY.format(
        email=email,
        year=year,
        month=month,
        BIGQUERY_EMPLOYEE_CAPACITY=BIGQUERY_EMPLOYEE_CAPACITY)

    return execute_query(query, error_value=[])


def register_employee_capacity(email, year, month, hours, office, capacity, realcapacity, fte, hiring_date, enddate):
    insert_query_builder = BigqueryUpdateQueryBuilder(
        email,
        year,
        month,
        hours,
        fte,
        office,
        capacity,
        hiring_date,
        enddate,
        realcapacity,
    )
    query = insert_query_builder.build_insert()

    return execute_query(query, error_value=[])


def update_employee_capacity(email, year, month, hours, office, capacity, realcapacity, fte, hiring_date, enddate):
    update_query_builder = BigqueryUpdateQueryBuilder(
        email,
        year,
        month,
        hours,
        fte,
        office,
        capacity,
        hiring_date,
        enddate,
        realcapacity
    )
    query = update_query_builder.build_update()

    return execute_query(query, error_value=[])


def create_or_update_employee(email, data):
    def _get_capacity_data(employee_capacity):
        capacity_data = {}
        for capacity in employee_capacity:
            capacity_data['fte'] = capacity.get('fte', 0.0)

        return capacity_data

    successfactor_data = data.pop('successfactor_data')
    employee_capacity = _get_capacity_data(get_employee_capacity(
        email,
        data['yearSelected'],
        data['monthSelected']))
    totalTimeSpent = data['data']['totalTimeSpent'] * 1000

    if employee_capacity:
        update_employee_capacity(
            email,
            data['yearSelected'],
            data['monthSelected'],
            totalTimeSpent,
            successfactor_data['office_name'],
            data['agreementHours']['totalHours'] * MS_FOR_HOUR,
            data['agreementHours']['realcapacity'] * MS_FOR_HOUR,
            successfactor_data['FTE'],
            successfactor_data.get('hiring_date'),
            successfactor_data.get('enddate'))
    else:
        register_employee_capacity(
            email,
            data['yearSelected'],
            data['monthSelected'],
            totalTimeSpent,
            successfactor_data['office_name'],
            data['agreementHours']['totalHours'] * MS_FOR_HOUR,
            data['agreementHours']['realcapacity'] * MS_FOR_HOUR,
            successfactor_data['FTE'],
            successfactor_data.get('hiring_date'),
            successfactor_data.get('enddate'))


def create_batch_insert_values(email, data):
    totalTimeSpent = data['data']['totalTimeSpent'] * 1000
    successfactor_data = data.pop('successfactor_data')
    enddate = successfactor_data.get('enddate')
    if enddate:
        enddate = f"'{enddate}'"
    else:
        enddate = 'null'

    return "('{email}','{yearSelected}','{monthSelected}',{totalTimeSpent},{fte},'{office}',{capacity},{realcapacity},'{startdate}',{enddate})".format(
        email=email,
        yearSelected=data["yearSelected"],
        monthSelected=data["monthSelected"],
        totalTimeSpent=totalTimeSpent,
        fte=successfactor_data["FTE"],
        office=successfactor_data["office_name"],
        capacity=data["agreementHours"]["totalHours"] * MS_FOR_HOUR,
        realcapacity=data["agreementHours"]["realcapacity"] * MS_FOR_HOUR,
        startdate=successfactor_data.get("hiring_date"),
        enddate=enddate,
    )


def insert_batch_capacities(capacities):
    query = f"INSERT INTO `{BIGQUERY_EMPLOYEE_CAPACITY}` (email, year, month, jira, fte, office, capacity, realcapacity, startdate, enddate) VALUES "
    values = ",".join(capacities)

    return execute_query(query + values)


def remove_data(year, month, office):
    query = f"DELETE FROM `{BIGQUERY_EMPLOYEE_CAPACITY}` WHERE year='{year}' AND month='{month}' AND office='{office}'"

    return execute_query(query, error_value=[])