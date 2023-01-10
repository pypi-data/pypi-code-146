import calendar


def show_calendar(year, month: int = None):
    if month:
        return calendar.month(year, month)
    else:
        return calendar.calendar(2023)


if __name__ == '__main__':
    print(show_calendar(2022))
