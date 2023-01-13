from pathlib import Path
import json
import numpy as np


def build_agregation(dir_path:str):
    flist = [p for p in Path(dir_path).iterdir() if p.is_file()]

    http600 = []
    http500 = []
    http400 = []
    http200 = []
    ticks = []

    number_retry = 0

    for file_path in flist:
        if not str(file_path).endswith(".json"):
            continue
        with open(file_path, encoding='utf8') as f:
            data = json.load(f)
            number_retry = number_retry + data["TryNumber"]
            status_code = data["StatusCode"]
            ticks.append(data["TicksAt"]/10000000)
            if status_code >= 600:
                p = Path(data["FileDirectory"])
                http500.append(p.stem)
            elif status_code >= 500:
                p = Path(data["FileDirectory"])
                http500.append(p.stem)
            elif status_code >= 400:
                p = Path(data["FileDirectory"])
                http400.append(p.stem)
            elif status_code == 200:
                http200.append(p.stem)


    startAt = np.min(ticks)
    endAt = np.max(ticks)

    result = {
        "total": len(flist),
        "number_retry": number_retry,
        "number200": len(http200),
        "number500": len(http500),
        "number600": len(http600),
        "number400": len(http400),
        "http600": http600,
        "http500": http500,
        "http400": http400,
        "elapsed_time_seconds": int(endAt-startAt)
    }
    return result

def create_summary(dir_path:str, output_file_path:str):
    result = build_agregation(dir_path)
    print(result)
    with open(output_file_path, "w") as out_file:
        json.dump(result, out_file, indent=6)


