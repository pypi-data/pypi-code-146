from collections import defaultdict


WEATHER_CODE_NAMES = defaultdict(lambda: "???")

WEATHER_CODE_NAMES.update(
    {
        0: "CLEAR SKY",
        1: "MAINLY CLEAR",
        2: "SOME CLOUDS",
        3: "OVERCAST",
        45: "FOG",
        48: "ICY FOG",
        51: "LIGHT DRIZZLE",
        53: "DRIZZLE",
        55: "DENSE DRIZZLE",
        61: "SLIGHT RAIN",
        63: "RAIN",
        65: "HEAVY RAIN",
        66: "FREEZING RAIN",
        67: "FREEZING DOWNPOUR",
        71: "LIGHT SNOW",
        73: "SNOW",
        75: "HEAVY SNOW",
        80: "LIGHT SHOWERS",
        81: "SHOWERS",
        82: "HEAVY SHOWERS",
        85: "LIGHT SNOW SHOWERS",
        86: "SNOW SHOWERS",
        95: "THUNDER",
        96: "THUNDER WITH LIGHT HAIL",
        99: "THUNDER WITH HAIL",
    }
)
