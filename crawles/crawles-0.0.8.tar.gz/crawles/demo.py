import re

import requests

from ThreadPool import ThreadPool

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}


class A(ThreadPool):
    def turn_pages(self):
        url_list = ['https://sc.chinaz.com/tupian/meinvxiezhen.html'] \
                   + [f'https://sc.chinaz.com/tupian/meinvxiezhen_{i}.html'
                      for i in range(2, 51)]
        yield url_list

    def get_data(self, url):
        html = requests.get(url, headers=headers)
        html.encoding = 'UTF-8-SIG'
        html_data = re.findall(
            '<div class="item">\s+<img src=".*?"\s+style=".*?"\s+data-original="(.*?)"\s+class="lazy"\s+alt="(.*?)"\s+/>',
            html.text, re.S)
        for index, image_data in enumerate(html_data, start=1):
            image_url, image_name = image_data
            yield [index, image_url, image_name]

    def save_data(self, args):
        print(args)


A(3, 5, 22)
