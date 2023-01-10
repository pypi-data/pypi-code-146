from datetime import datetime, timedelta


def get_wy(dates, wy_month=7, using_end_year=True):
    """
    Returns water years, as a list of ints, for a given array of dates. Use this to
    add water year info into a pandas DataFrame. 

    The default (using_end_year==True) follows the convention used for fiscal years, 
    whereby water years are labelled based on their end dates. E.g. the 2022 water 
    year is from 2021-07-01 to 2022-06-30 inclusive. This has the advantage that 
    results from the period, e.g. annual totals, are determined in the calendar year 
    corresponding to the water year. The alternative (using_end_year==False) will 
    report based on the start of the period.
    """
    if using_end_year:
        answer = [d.year if d.month < wy_month else d.year + 1 for d in dates]
    else:
        answer = [d.year + 1 if d.month < wy_month else d.year for d in dates]        
    return answer


def get_dates(start_date, end_date=None, days=0, years=1, include_end_date=False):
    """
    Generates a list of daily datetime values from a given start date. The length 
    may be defined by an end_date, or a number of days, or a number of years. This 
    function may be useful for working with daily datasets and models.
    """
    if (days > 0):
        # great, we already have the number of days
        pass
    elif (end_date != None):
        # use end_date
        days = (end_date - start_date).days
        days = days + 1 if include_end_date else days
    else:
        # use years
        end_date = datetime(start_date.year + years, start_date.month, start_date.day,
            start_date.hour, start_date.minute, start_date.second, start_date.microsecond)
        days = (end_date - start_date).days
    date_list = [start_date + timedelta(days=x) for x in range(days)]
    return date_list