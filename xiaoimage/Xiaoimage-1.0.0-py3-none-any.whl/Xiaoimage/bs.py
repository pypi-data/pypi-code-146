from bs4 import BeautifulSoup
import requests
import os
import urllib.request
import time
import sys
def main():
    try:
        url = sys.argv[1]
        path = sys.argv[2]
        get_links(url, path)
    except Exception as e:
        print('Error: {}'.format(e))
        sys.exit(0)
headers = {
    "Cookie": "UM_distinctid=16685e0279d3e0-06f34603dfa898-36664c08-1fa400-16685e0279e133; bdshare_firstime=1539844405694; gsScrollPos-1702681410=; CNZZDATA1254092508=1744643453-1539842703-%7C1539929860; _d_id=0ba0365838c8f6569af46a1e638d05",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
}
def get_links(url, path):
    wb_data = requests.get(url, headers=headers)  # 加入 headers，避免被网站的反爬机制认为是蜘蛛
    wb_data.encoding = "utf-8"
    soup = BeautifulSoup(wb_data.text, 'lxml')
    links = soup.select("img")
    if not os.path.exists(path):  # 判断该文件夹是否存在，不存在则创建
        os.mkdir(path)
    i = 0
    for link in links:
        try:
            i += 1
            time.sleep(1)#暂停一秒，避免访问过快被反爬机制认为是蜘蛛
            img = link.get("src")
            img_name = link.get("alt")
            if img_name == None:
                img_name = i
            urllib.request.urlretrieve(img, "{}{}.jpg".format(path, img_name))
            print("-------- downloading image ---------")
        except Exception as e:
            print(f"Error: {e}")
    print("------ download done -------")
def html_load(url, ob):
    print('Collecting {}...'.format(url))
    urllib.request.urlretrieve(url, ob)
    print('secessly.')
