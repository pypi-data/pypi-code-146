from coronado import TripleEnum


# *** classes and objects ***

class DateRange(TripleEnum):
    """
    Date range presets for various triple operations.
    """
    CM = "CM"
    """
    Current month.
    """

    CUSTOM = "CUSTOM"
    """
    Custom date range defined with `startDate` and `endDate` request parameters.
    """

    P30D = "P30D"
    """
    Past 30 days.
    """

    P90D = "P90D"
    """
    Past 90 days.
    """

    P180D = "P180D"
    """
    Past 180 days.
    """

    YTD = "YTD"
    """
    Year-to-date.
    """

    LIFETIME = "LIFETIME"
    """
    From the start of triple enrollment until the present.
    """

