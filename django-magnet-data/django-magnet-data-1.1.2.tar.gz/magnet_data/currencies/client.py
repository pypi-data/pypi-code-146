# standard library
from urllib.request import Request
from urllib.request import urlopen
import datetime
import json

# django
from django.apps import apps

# magnet data
from magnet_data.currencies.urls import API_URL


def get_url(year: int, month: int, base_currency: str, counter_currency: str) -> str:
    """
    Obtain the api url to get all the values of {base_currency} as {counter_currency}
    on month {month} of the year {year}
    """
    base_currency = base_currency.lower()
    counter_currency = counter_currency.lower()

    if month < 10:
        month = "0{}".format(month)

    return f"{API_URL}{base_currency}/{counter_currency}/{year}/{month}/"


def update_values(year: int, month: int, base_currency: str,
                  counter_currency: str) -> None:
    """
    Obtain all values of the {month}-{year} month from {base_currency} to
    {counter_currency}
    """
    url = get_url(year, month, base_currency, counter_currency)

    request = Request(url)

    response = urlopen(request)
    data = json.loads(response.read())

    for values_data in data["objects"]:
        date_string = values_data["date"]
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()

        CurrencyValue = apps.get_model(
            app_label='magnet_data',
            model_name='CurrencyValue'
        )

        CurrencyValue.objects.update_or_create(
            date=date,
            base_currency=base_currency,
            counter_currency=counter_currency,
            defaults={
                "value": values_data["value"],
            },
        )
