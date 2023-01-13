# apisパッケージ用の初期化スクリプト
# 
# Copyright (c) 2022 Atsush Shibata(shivata@m-info.co.jp)
#
# Released under the MIT license.

from datetime import datetime
from json import loads
import requests
from bs4 import BeautifulSoup
import numpy as np

from IPython.display import display, HTML
import json



def doomsday_clock(year):
    dc_url = "https://ja.wikipedia.org/wiki/%E4%B8%96%E7%95%8C%E7%B5%82%E6%9C%AB%E6%99%82%E8%A8%88"
    resp = requests.get(dc_url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    secs = {}

    table = [x for x in soup.find_all("table", class_="wikitable")]
    for n, tr in enumerate(table[0].find_all("tr")):
        if n > 1:
            tds = [x for x in tr.find_all("td")]
            mstr = tds[1].text.replace("前", "")
            smstr = mstr.split("分")
            sec = 0
            if smstr[1]:
                sec = int(smstr[0])*60+int(smstr[1].replace("秒", ""))
            else:
                sec = int(smstr[0])*60
            secs[int(tds[0].text.replace("年", ""))] = sec

    if year in secs:
        return secs[year]
    else:
        return "不明"


def get_number_of_space_satellite():
    resp = requests.get("https://www.ucsusa.org/media/11490")
    lines = len(resp.text.split("\n"))-1
    return(lines)


def get_stock_price_prediction():
    """
    ランダムな[-1, 1]のうちランダムに数値を返す
    """
    return choice([-1, 1])


def get_wf_json(code=13):
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{code:02}0000.json"
    resp = requests.get(url)
    d = loads(resp.text)
    return d


def get_humid():
    """
    Open Metroから東京の直近の湿度を取得して返す
    """
    url = "https://api.open-meteo.com/v1/forecast?latitude=35.69&longitude=139.69&hourly=relativehumidity_2m"
    resp = requests.get(url)
    d = loads(resp.text)
    return d['hourly']['relativehumidity_2m'][0]



def get_bp():
    """
    Open Metroから東京の直近の気圧(日時)を取得して返す
    """
    url = "https://api.open-meteo.com/v1/forecast?latitude=35.69&longitude=139.69&hourly=surface_pressure"
    resp = requests.get(url)
    d = loads(resp.text)
    bp = d['hourly']['surface_pressure']
    [bp[i] for i in range(0, len(bp), 24)]


def get_rp(code=13):
    """
    codeにある地域(デフォルトは東京)の
    直近の降水確率を返す
    """
    d = get_wf_json(code)
    return int(d[0]["timeSeries"][1]["areas"][0]["pops"][0])


def get_temp(code=13):
    """
    codeにある地域(デフォルトは東京)の
    直近の気温予測を返す
    """
    d = get_wf_json(code)
    c = int(d[0]["timeSeries"][2]["areas"][0]["temps"][0])
    return int(1.8*c+32)


def f2c(f):
    """
    華氏(Fahrenheit)から摂氏(Celsius)に変換
    """
    return int((f-32)*(5/9))


def get_rpl(code=13):
    """
    codeにある地域(デフォルトは東京)の直近の降水確率を返す
    6時間ごと，4つ
    """
    d = get_wf_json(code)
    return [int(x) for x in d[0]["timeSeries"][1]["areas"][0]["pops"]][:4]


def get_wi():
    """
    東京の気温と湿度から，洗濯指数を得る。
    """
    tokyo_humid = humid()
    temp_f = temp()
    temp_c = f2c(temp_f)
    wi = 0.01*tokyo_humid
    wi = wi*(0.99*temp_c-14.3)
    wi = wi+0.81*temp_c+46.3
    return wi


def get_wr_index(code=13):
    """
    東京の今日の天気を，インデックスで返す
    1:晴れ，2:曇り，3:雨，4:雪
    """
    d = get_wf_json(code)
    return int(d[0]["timeSeries"][0]["areas"][0]["weatherCodes"][0][0])


def get_eq_info():
    dc_url = "https://api.p2pquake.net/v2/jma/quake?limit=1"
    resp = requests.get(dc_url)
    ql = loads(resp.text)
    q = ql[0]
    return q.get("earthquake", {})


def dict_print(jstr):
    """
    JSON相当の文字列，またはオブジェクトを受け取り，
    JSONを展開可能な状態で表示する関数。colabのみ対応。
    based on : https://gist.github.com/korakot/072f1ea70d3c3267ff2c64b61d78c89c
    """
    if type(jstr) != str:
        jstr = json.dumps(jstr)
    return HTML("""
<script src="https://rawgit.com/caldwell/renderjson/master/renderjson.js"></script>
<script>
renderjson.set_show_to_level(1)
document.body.appendChild(renderjson(%s))
new ResizeObserver(google.colab.output.resizeIframeToContent).observe(document.body)
</script>
""" % jstr)



def get_eq_info2():
    """
    api.p2pquake.netから，日本で発生した直近の地震の情報を取り出す
    戻り値は辞書
    """
    # 地震の情報を読み込む
    url = "https://api.p2pquake.net/v2/jma/quake?limit=1"
    r = requests.get(url)
    ql = loads(r.text)
    dt = ql[0]["created_at"]
    dto = datetime.strptime(ql[0]["created_at"].split(".")[0], "%Y/%m/%d %H:%M:%S")
    retd = ql[0]["earthquake"]["hypocenter"]
    retd["datetime"] = dto
    return retd


