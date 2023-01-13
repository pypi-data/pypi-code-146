# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from tools_hjh.ThreadPool import ThreadPool


def main():
    tp = ThreadPool(2, save_result=True)
    chrome_path = r'U:\MyApps\CentBrowser\App\chrome.exe'
    chromedriver_path = r'U:\MyApps\CentBrowser\chromedriver.exe'

    cp = ChromePool(2, chrome_path=chrome_path, chromedriver_path=chromedriver_path)
    u1 = tp.run(cp.get, ('https://www.baidu.com',))
    time.sleep(1)
    u2 = tp.run(cp.get, ('https://www.yeah.net',))
    
    tp.wait()
    print(len(tp.get_result(u1)), len(tp.get_result(u2)))
    cp.close()


class Chrome():
    """ 使用浏览器解析url，返回源码
        __init__.param：
            chrome_path: chrome.exe路径
            chromedriver_path: chromedriver.exe路径
    """

    def __init__(self, chrome_path, chromedriver_path, is_hidden=False, is_display_picture=True, proxies=None):
        chrome_options = Options()
        if is_hidden:
            chrome_options.add_argument("--headless")
        chrome_options.binary_location = chrome_path
        if not is_display_picture:
            chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
        self.chrome = webdriver.Chrome(chromedriver_path, options=chrome_options)
        self.status = 0  # 未被占用
        
    def close(self):
        self.chrome.quit()
        
    def get(self, url, headers=None, data=None):
        self.status = 1  # 被占用
        self.chrome.get(url)
        text = self.chrome.page_source
        self.status = 0
        return text
    
    def get_status(self):
        return self.status


class ChromePool():

    def __init__(self, maxSize, chrome_path, chromedriver_path, is_hidden=False, is_display_picture=True, proxies=None):
        self.maxSize = maxSize
        self.pool = []
        for _ in range(0, maxSize):
            self.pool.append(Chrome(chrome_path, chromedriver_path, is_hidden, is_display_picture, proxies))
        self.openSize = 0
            
    def get(self, url, headers=None, data=None):
        while self.openSize == self.maxSize:
            time.sleep(0.2)
        for chrome in self.pool:
            if chrome.get_status() == 0:
                self.openSize = self.openSize + 1
                text = chrome.get(url, headers, data)
                chrome.get(url='data:,')
                self.openSize = self.openSize - 1
                return text
        time.sleep(0.2)
        return self.get(url, headers, data)
    
    def close(self):
        while self.openSize > 0:
            time.sleep(0.2)
        for c in self.pool:
            c.close()


if __name__ == '__main__':
    main()
