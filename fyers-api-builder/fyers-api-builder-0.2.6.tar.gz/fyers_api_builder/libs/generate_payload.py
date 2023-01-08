def generate_payload(symbol, resolution, range_from, range_to):
    return {
        "symbol": symbol,
        "resolution": resolution,
        "date_format": 0,
        "range_from": range_from,
        "range_to": range_to,
        "cont_flag": "1",
    }
