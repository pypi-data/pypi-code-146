from django.apps import apps
from magnet_data.currencies.currency_pair import CurrencyPair
from magnet_data.currencies.enums import CurrencyAcronyms
from magnet_data.holidays.enums import Countries
from magnet_data import utils
import datetime


class Currencies(CurrencyAcronyms):
    @staticmethod
    def get_pair(base_currency: str, counter_currency: str) -> CurrencyPair:
        """
        Returns a CurrencyPair object
        """
        return CurrencyPair(
            base_currency=base_currency,
            counter_currency=counter_currency
        )


class Holidays(Countries):
    def __init__(self):
        self.last_updated = None
        self.cls = apps.get_model(
            app_label='magnet_data',
            model_name='Holiday'
        )

    def update(self, country_code: str):
        """
        Update values stored in the database with what the api returned
        """
        now = datetime.datetime.now()
        threshold = now - datetime.timedelta(1)
        if self.last_updated is None or self.last_updated < threshold:
            self.last_updated = now
            self.cls.update_holidays(country_code=country_code.upper())

    def is_workday(self, date, country_code: str):
        """
        Returns True if the given date is not Saturday, Sunday, or
        Holiday
        Keyword arguments:
            from_date -- date to check
            country-code -- de ISO 3166 country code
        """
        self.update(country_code)
        if date.weekday() == 5:  # Saturday
            return False

        if date.weekday() == 6:  # Sunday
            return False

        return not self.cls.objects.filter(
            date=date,
            country_code=country_code.upper(),
        ).exists()

    def get_next_working_day(self,
                             country_code: str,
                             working_days: int = 1,
                             from_date: datetime.date = None,
                             step: int = 1):
        """
        Returns the next date that is a working day.
        Keyword arguments:
            country-code -- de ISO 3166 country code
            working_days -- number of working days to count (default 1)
            from_date -- date to start counting from (default today)
            step -- the amount by which the index increases. (default 1)
        """
        def is_workday(date):
            """
            Returns True if the given date is not Saturday, Sunday, or
            Holiday
            """
            if date.weekday() in (5, 6):  # Saturday or Sunday
                return False

            return not self.cls.objects.filter(
                date=date,
                country_code=country_code.upper(),
            ).exists()

        self.update(country_code)

        if from_date is None:
            from_date = utils.today()

        final_date = from_date

        while working_days > 0:
            final_date += datetime.timedelta(days=step)

            if is_workday(final_date):
                working_days -= 1

        return final_date

    def get_holidays_count_during_weekdays(self,
                                           country_code: str,
                                           start_date: datetime.date,
                                           end_date: datetime.date):
        """
        Returns the number of holidays between to days, not considering
        saturdays and sundays
        Keyword arguments:
            country-code -- de ISO 3166 country code
            start_date -- date to start counting from
            end_date -- date where to stop counting
        """
        self.update(country_code)
        days = 0

        holidays_dates = self.cls.objects.filter(
            date__range=[start_date, end_date],
            country_code=country_code.upper(),
        ).values_list('date', flat=True)

        for date in holidays_dates:
            if date.weekday() not in (5, 6):  # not in sunday or saturday
                days += 1

        return days


class MagnetDataClient:
    def __init__(self) -> None:
        super().__init__()
        self.currencies = Currencies()
        self.holidays = Holidays()
