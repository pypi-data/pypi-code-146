from ms_imputedhours_core.agreements import Agreements
from ms_imputedhours_core.employee import get_real_fte, calculate_real_capacity
from ms_imputedhours_core.office import get_real_office_name
from ms_imputedhours_core.employee.data.bigquery import (
    get_successfactor_all_data,
    get_all_data,
    get_all_data_by_dates,
    get_all_employee_capacity,
    get_imputed_hours,
)
from ms_imputedhours_core.employee.data.helpers.alert import should_exclude_employee
from ms_imputedhours_core.employee.data.transformers.hours import (
    transform_all_capacities,
    transform_successfactor_all_data,
    group_task_by_email,
)

AGREEMENTS_SPREADSHEET_ID = '1gMQ30Sl0QHhocTQgbYpWvS6DarhcRIeBIANW8FYLTTQ'
AWAIT_FOR_GOOLE_API_BACK_PRESSURE = 5
EMPTY_SUCCESSFACTOR_DATA = {'office_name': '', 'FTE': 0, 'hiring_date': None, 'enddate': None}
EMPTY_AGREEMENT_HOURS_DATA = {'totalHours': 0.0, 'days': {}}
EMPTY_EMPLOYEE_DATA = {
    'data': {},
    'yearSelected': 0,
    'monthSelected': 0,
    'agreementHours': 0,
    'successfactor_data': EMPTY_SUCCESSFACTOR_DATA,
}
GOOGLE_API_MAX_REQUESTS_PER_SEG = 60


def get_all_employees_monthly_data_by_office(date, office_name):
    data = {}
    agreement_hours = Agreements(AGREEMENTS_SPREADSHEET_ID)\
        .get_hours_by_month(date.month, date.year, office_name)
    successfactor_all_data = transform_successfactor_all_data(
        get_successfactor_all_data(office_name))
    if successfactor_all_data:
        office_emails = successfactor_all_data.keys()
        current_month_data = group_task_by_email(
            get_all_data(date, office_emails))
        all_employee_ftes = transform_all_capacities(
            get_all_employee_capacity(date.month, date.year))

        for email in office_emails:
            successfactor_data = successfactor_all_data.get(
                email, EMPTY_SUCCESSFACTOR_DATA)

            if should_exclude_employee(email, date, successfactor_data['hiring_date'], successfactor_data['enddate']):
                continue

            office_name = get_real_office_name(
                successfactor_data.get('office_name'))

            fte = get_real_fte(successfactor_data,
                               all_employee_ftes.get(email), date)

            real_capacity = calculate_real_capacity(
                agreement_hours,
                successfactor_data.get('hiring_date'),
                successfactor_data.get('enddate'),
                date,
                date,
                fte,
            )

            # Updating fte value
            successfactor_data['FTE'] = fte
                
            if email not in data.keys():
                data[email] = {
                    'data': {'totalTimeSpent': current_month_data.get(email, {}).get('totalHours', 0)},
                    'agreementHours': {'totalHours': agreement_hours.get('totalHours', 0), 'realcapacity': real_capacity},
                    'successfactor_data': successfactor_data,
                    'yearSelected': date.year,
                    'monthSelected': date.month,
                }

    return data


def get_all_employee_data_by_range(from_date, to_date, office_name):
    employees_data = {}
    agreement_hours = Agreements(AGREEMENTS_SPREADSHEET_ID)\
        .get_hours_by_range(from_date, to_date, office_name)
    successfactor_all_data = transform_successfactor_all_data(
        get_successfactor_all_data(office_name))
    office_emails = successfactor_all_data.keys()
    current_month_data = group_task_by_email(
        get_all_data_by_dates(from_date, to_date,  office_emails))
    all_employee_ftes = transform_all_capacities(
        get_all_employee_capacity(from_date.month, from_date.year))

    for email in office_emails:
        successfactor_data = successfactor_all_data.get(
            email, EMPTY_SUCCESSFACTOR_DATA)
        
        if should_exclude_employee(email, from_date, successfactor_data['hiring_date'], successfactor_data['enddate']):
            continue

        employee_fte = get_real_fte(
            successfactor_data, all_employee_ftes.get(email), from_date)
        employee_current_capacity = current_month_data.get(
            email, EMPTY_AGREEMENT_HOURS_DATA)['totalHours'] / 3600
        employee_real_capacity = calculate_real_capacity(
            agreement_hours,
            successfactor_data.get('hiring_date'),
            successfactor_data.get('enddate'),
            from_date,
            to_date,
            employee_fte,
            calculate_range=True
        )

        capacity_percentage = 0
        if employee_current_capacity > 0 and employee_real_capacity:
            capacity_percentage = round(
                (employee_current_capacity * 100) / employee_real_capacity, 2)

        # print("""
        # Email: {}
        # FTE: {}
        # REAL CAPACITY: {}
        # CAPACITY: {}
        # Percentage imputed: {}
        # Supervisor: {}
        # """.format(email, employee_fte, employee_real_capacity, employee_current_capacity, capacity_percentage, successfactor_data['supervisor']))
        # print(current_month_data.get(email, EMPTY_AGREEMENT_HOURS_DATA))
        # print("\n")

        employees_data[email] = {
            'real_capacity': employee_real_capacity,
            'current_capacity': employee_current_capacity,
            'current_percentage_hours_imputed': capacity_percentage,
            'supervisor': successfactor_data['supervisor'],
            'name': successfactor_data['name'],
        }

    return employees_data


def get_all_imputations_per_day(from_date, to_date):
    current_month_data = group_task_by_email(
        get_imputed_hours(from_date, to_date))

    return current_month_data
