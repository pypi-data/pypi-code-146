from ms_imputedhours_core.employee.data.constants import EXCLUDE_ALERT_EMAILS


def should_exclude_employee(email, date, hired_date, end_date):
    is_email_excluded = email in EXCLUDE_ALERT_EMAILS
    
    is_personal_email = "@makingscience" not in email
    
    is_enddate_before_date = end_date and (end_date.year, end_date.month) <= (date.year, date.month)
    
    is_hired_date_after_date = hired_date and (hired_date.year, hired_date.month) >= (date.year, date.month)

    return is_email_excluded or is_enddate_before_date or is_hired_date_after_date or is_personal_email
    