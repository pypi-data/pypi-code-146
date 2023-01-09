from datetime import datetime

HUNDRED_PERCENT = 100


def get_real_fte(successfactor_data, employeeFTE, date):
    today = datetime.today()
    is_past_date = (date.year, date.month) <= (today.year, today.month)
    try:
        # Some employees has null as FTE.
        fte = successfactor_data['FTE'] / HUNDRED_PERCENT
    except Exception:
        fte = HUNDRED_PERCENT

    if employeeFTE and is_past_date:
        fte = employeeFTE['fte']

    return fte

def calculate_real_capacity(agreement_hours, hiringdate, end_date, date, to_date, fte, calculate_range=False):
    def _is_date_before_hired():
        return hiringdate and ((date.year, date.month) < (hiringdate.year, hiringdate.month))

    def _is_date_same_hired():
        return hiringdate and ((date.year, date.month) == (hiringdate.year, hiringdate.month))

    def _is_date_between_hired_and_end_date():
        is_date_before_end_date = not end_date or (
            (date.year, date.month) < (end_date.year, end_date.month))
        return is_date_before_end_date and hiringdate and ((date.year, date.month) > (hiringdate.year, hiringdate.month))

    def _is_date_same_end_date():
        return end_date and ((date.year, date.month) == (end_date.year, end_date.month))

    def _is_date_after_end_date():
        return end_date and (date.year, date.month) > (end_date.year, end_date.month)

    real_capacity = agreement_hours.get('totalHours', 0)

    if _is_date_before_hired():
        # Months prior to hiring the employee
        real_capacity = 0
    elif _is_date_same_hired():
        # Same month of hiring the employee
        real_capacity = 0
        days = agreement_hours.get('days', {})

        for day, hours in days.items():
            if (int(day) >= hiringdate.day):
                real_capacity += float(hours.replace(',', '.'))
    elif calculate_range and _is_date_between_hired_and_end_date():
        # Just when we want to calculate hours by range of date
        real_capacity = 0
        days = agreement_hours.get('days', {})
        for dayMonth, hours in days.items():
            day, month = dayMonth.split('-')
            is_date_after_from = (int(day), int(
                month)) >= (date.day, date.month)
            is_date_before_to = (int(day), int(month)) <= (
                to_date.day, to_date.month)
            if is_date_after_from and is_date_before_to:
                real_capacity += float(hours.replace(',', '.'))

    if _is_date_same_end_date():
        # Same month of the termination of the employment contract
        real_capacity = 0
        days = agreement_hours.get('days', {})
        for day, hours in days.items():
            if (int(day) <= end_date.day):
                real_capacity += float(hours.replace(',', '.'))

    elif _is_date_after_end_date():
        # Months after the termination of the employee's contract
        real_capacity = 0

    return real_capacity * fte
