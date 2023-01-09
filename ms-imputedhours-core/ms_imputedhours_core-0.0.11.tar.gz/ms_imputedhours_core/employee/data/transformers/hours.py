EMPTY_FTE = '0'


def transform_successfactor_data(bigquery_successfactor):
    data_json = {
        'office_name': 'Madrid - Ing',
        'FTE': 1,
    }

    for data in bigquery_successfactor:
        data_json['office_name'] = data.get('office', '')
        data_json['FTE'] = data.get('fte', 0)

    return data_json


def transform_successfactor_all_data(bigquery_successfactor):
    data_json = {}

    for data in bigquery_successfactor:
        email = data.get('email', '')
        hiringdate = data.get('hiringdate', '')
        enddate = data.get('internshipdate', '')

        if email not in data_json.keys():
            data_json[email] = {}

        fte = data.get('fte', EMPTY_FTE) or EMPTY_FTE  # For null values
        data_json[email]['supervisor'] = data.get('supervisor', '')
        data_json[email]['office_name'] = data.get('office', '')
        data_json[email]['FTE'] = float(fte.replace(',', '.'))
        data_json[email]['hiring_date'] = hiringdate
        data_json[email]['enddate'] = enddate
        data_json[email]['name'] = "{} {}".format(data.get('name', ''), data.get('lastname', ''))

    return data_json


def transform_all_capacities(capacities):
    data_json = {}

    for data in capacities:
        email = data.get('email')
        if email not in data_json:
            data_json[email] = {
                'fte': data.get('fte')
            }

    return data_json


def group_task_by_email(month_data):
    data_by_email = {}
    for task in month_data:
        taskTimeSpent = task.get('timeSpent', 0)
        taskEmail = task.get('authorEmail')
        taskStarted = task.get('started')

        if taskEmail not in data_by_email.keys():
            data_by_email[taskEmail] = {'totalHours': 0, 'days': {}}

        if taskStarted.day not in data_by_email[taskEmail]['days']:
            data_by_email[taskEmail]['days'][taskStarted.day] = 0

        data_by_email[taskEmail]['totalHours'] += taskTimeSpent
        data_by_email[taskEmail]['days'][taskStarted.day] += taskTimeSpent

    return data_by_email
