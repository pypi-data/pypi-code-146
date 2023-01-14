import datetime
import os

from collections import defaultdict

import jinja2
import requests

from .config import WEATHER_CODE_NAMES

ISO_LOCAL_FORMAT = "%Y-%m-%dT%H:%M"
ISO_DATE_FORMAT = "%Y-%m-%d"
URL_PATTERN = "https://api.open-meteo.com/v1/forecast?latitude=%f&longitude=%f&hourly=temperature_2m,apparent_temperature,precipitation,weathercode"


def get_images(folder):
    try:
        images = os.listdir(folder)
    except:
        images = []
    actual_images = {
        int(image.split(".")[0]): image
        for image in images
        if image.endswith("png")
    }
    d = defaultdict(lambda: "XXX.png")
    d.update(actual_images)
    return d


def format_data(raw_data):
    timestamps = raw_data["hourly"]["time"]
    lookup = {}
    for i, timestamp in enumerate(timestamps):
        row = {key: raw_data["hourly"][key][i] for key in raw_data["hourly"]}
        lookup[timestamp] = row

    days = list(set(timestamp.split("T")[0] for timestamp in timestamps))
    days.sort()
    day_list = []
    for day in days:
        hours = list(
            set(timestamp for timestamp in timestamps if timestamp.split("T")[0] == day)
        )
        hours.sort()
        hour_list = [lookup[timestamp] for timestamp in hours]
        day_data = {
            "date": day,
            "hours": hour_list,
        }
        day_list.append(day_data)

    return day_list


def make_day_names(today):
    return {
        today.strftime(ISO_DATE_FORMAT): "TODAY",
        (today + datetime.timedelta(days=1)).strftime(ISO_DATE_FORMAT): "TOMORROW",
        (today + datetime.timedelta(days=2)).strftime(ISO_DATE_FORMAT): (today + datetime.timedelta(days=2)).strftime("%A").upper(),
        (today + datetime.timedelta(days=3)).strftime(ISO_DATE_FORMAT): (today + datetime.timedelta(days=3)).strftime("%A").upper(),
    }


def render_weather(location, template, image_folder):
    url = URL_PATTERN % location
    result = requests.get(url)
    result.raise_for_status()
    raw_data = result.json()
    data = format_data(raw_data)

    now = datetime.datetime.now()
    this_hour = datetime.datetime(now.year, now.month, now.day, now.hour)
    extra = {
        "timestamp": now.strftime(ISO_LOCAL_FORMAT),
        "hour": this_hour.strftime(ISO_LOCAL_FORMAT),
        "names": WEATHER_CODE_NAMES,
        "images": get_images(image_folder),
        "day_names": make_day_names(datetime.date.today()),
    }

    env = jinja2.Environment(loader=jinja2.PackageLoader("meteo_render"))
    env.globals.update(zip=zip)
    template = env.get_template(os.path.join(template, "page.html.j2"))

    return template.render(data=data, extra=extra)
