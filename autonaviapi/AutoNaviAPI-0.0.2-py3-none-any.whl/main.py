__version__ = "1.0.0"

import json
import requests
from time import strftime, gmtime


def get_location(KEY, CITY, ADDRESS, OUTPUT="json"):
    url = 'http://restapi.amap.com/v3/geocode/geo?parameters'
    params = {
        'city': CITY,
        'address': ADDRESS,
        'key': KEY,
        'output': OUTPUT}
    j = json.loads(requests.get(url, params).content)
    return j


def unget_location(KEY, LOCATION, OUTPUT="json", EX="BASE", RADIUS=3000):
    url = 'https://restapi.amap.com/v3/geocode/regeo'
    params = {
        "location": LOCATION,
        "output": OUTPUT,
        "key": KEY,
        'radius': RADIUS,
        'extensions': EX}
    response = requests.get(url, params=params)
    answer = response.json()
    return answer


def driver(key, origin, destination, extensions="base"):
    url = "	https://restapi.amap.com/v3/direction/driving?parameters"
    params = {
        "key": key,
        "origin": origin,
        "destination": destination,
        "extensions": extensions
    }
    response = requests.get(url, params=params)
    answer = response.json()
    return answer


def walk(key, origin, destination, output="json"):
    url = "https://restapi.amap.com/v3/direction/walking?parameters"
    params = {
        "key": key,
        "origin": origin,
        "destination": destination,
        "OUTPUT": output
    }
    response = requests.get(url, params=params)
    answer = response.json()
    return answer


def ride(key, origin, destination):
    url = "	https://restapi.amap.com/v4/direction/bicycling?parameters"
    params = {
        "key": key,
        "origin": origin,
        "destination": destination,
    }
    response = requests.get(url, params=params)
    answer = response.json()
    return answer


if __name__ == "__main__":
    try:
        while True:
            KEY = str(input("请输入密钥(如果没有请输入：无):"))
            if KEY != "":
                break
            if KEY == "无":
                KEY = 'cbf50c4fd937fd427bffafa8700615a6'
        CITY = str(input("请输入起点(市、自治州、自治县、县):"))
        CITY2 = str(input("请输入终点(市、自治州、自治县、县):"))
        ADDRESS = str(input("请输入起点(村庄、小区):"))
        ADDRESS2 = str(input("请输入终点(村庄、小区):"))
        OUTPUT = 'json'
        old_location = get_location(KEY=KEY, CITY=CITY, ADDRESS=ADDRESS, OUTPUT=OUTPUT)[
            "geocodes"][0]["location"]
        location = get_location(KEY=KEY, CITY=CITY2, ADDRESS=ADDRESS2, OUTPUT=OUTPUT)[
            "geocodes"][0]["location"]
        with open("API_get.txt", "w", encoding="utf-8") as file:
            file.write(str(driver(KEY, location, old_location)))

        with open("API_get.txt", "r", encoding="utf-8") as file:
            content = eval(file.read())

            if content["status"] == "0":
                print("Error")
            else:
                longs = int(content["route"]["paths"][0]["distance"])
                if longs > 1000:
                    longs = longs//1000
                    tmp = longs % 1000/10
                    longs = float(longs) + tmp
                    print("距离:", longs, "千米")
                else:
                    print("距离:", longs, "米")
                times = strftime("%H:%M:%S", gmtime(
                    int(content["route"]["paths"][0]["duration"])))
                tolls = int(content["route"]["paths"][0]["tolls"])
                traffic_lights = int(
                    content["route"]["paths"][0]["traffic_lights"])
                print("预计时间:", times)
                print("过路费:", tolls, '元')
                print("共", traffic_lights, "个红绿灯")
                for i in range(len(content["route"]["paths"][0]["steps"])):
                    tmp = content["route"]["paths"][0]["steps"][i]["instruction"]
                    print(tmp)
    except KeyError as e:
        print("\n出错了，可能是输入的的地点不存在，或密钥不正确。")
    except Exception as e:
        print("\n出错了，但未找到原因，请参考", e)
    except KeyboardInterrupt:
        print("\n请不要在运行时按下Ctrl+C")
