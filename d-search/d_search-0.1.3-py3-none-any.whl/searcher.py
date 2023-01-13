import requests
import re
import json
import time
from typing import List, Optional
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from pydantic import conint, validate_arguments
from .utils import normalize_html_text
from .data import Question, Item, Info, Image
from pathlib import Path
from logging import getLogger

log = getLogger()


def get_driver(save_path: Optional[str] = None, headless: bool = True):
    """获取chrome浏览器驱动"""
    options = ChromeOptions()
    if headless:
        options.add_argument('headless')
    if save_path:
        appState = """{"recentDestinations": [{"id": "Save as PDF","origin": "local"}],"mediaSize": {"height_microns": 279400,"name": "NA_LETTER","width_microns": 215900,"custom_display_name": "Letter"},"selectedDestinationId": "Save as PDF","version": 2,"isHeaderFooterEnabled": false}"""
        appState = json.loads(appState)
        profile = {'printing.print_preview_sticky_settings.appState': json.dumps(appState),'savefile.default_directory': save_path,'download.default_directory': save_path}
        options.add_experimental_option('prefs', profile)
        # 该参数必须存在，不设置会无法使用打印，保存全屏图片等功能
        options.add_argument('--kiosk-printing')
    driver = Chrome(options=options)
    return driver


def scroll_to_bottom(driver):
    """将窗口一点一点滑动到底部，方便加载图片
    """
    js = "return action=document.body.scrollHeight"
    # 初始化现在滚动条所在高度为0
    height = 0
    # 当前窗口总高度
    new_height = driver.execute_script(js)
    while height < new_height:
        # 将滚动条调整至页面底部
        for i in range(height, new_height, 300):
            driver.execute_script('window.scrollTo(0, {})'.format(i))
            time.sleep(0.3)
        height = new_height
        new_height = driver.execute_script(js)


class BaiduPedia:
    """百度百科
    """
    item_base_url = "https://baike.baidu.com/item/"
    search_base_url = 'https://baike.baidu.com/search?word='
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36' }        
    def __init__(self, headless: bool = True) -> None:
        self.driver = get_driver(headless=headless)

    def _get_item_url(self, item_query: str) -> str:
        return self.item_base_url + item_query
        
    def _get_item_summary(self, driver) -> str:
        """获取该词条的简介
        """
        summary = driver.find_element(by=By.CLASS_NAME, value='lemma-summary')
        return summary.text
    
    def _get_item_desc(self, driver) -> str:
        """获取该词条的描述
        """
        desc = driver.find_element(by=By.CLASS_NAME, value='lemma-desc')
        return desc.text
    
    def _get_item_name(self, driver) -> str:
        """获取该词条中的名称
        """
        item_name = driver.find_element(by=By.CSS_SELECTOR, value='h1')
        return item_name.text
    
    def _get_item_synonyms(self, driver) -> List[str]:
        """获取该词条的所有同义词
        """
        synonyms = driver.find_elements(by=By.CLASS_NAME, value='viewTip-fromTitle')
        return [s.text for s in synonyms]
    
    def _get_item_info(self, driver) -> List[Info]:
        """获取该词条的知识三元组
        """
        info_ls = []
        keys = driver.find_elements(by=By.CLASS_NAME, value='basicInfo-item.name')
        values = driver.find_elements(by=By.CLASS_NAME, value='basicInfo-item.value')
        for i, k in enumerate(keys):
            key = k.text
            vs = '\n'.join(values[i].text.split('、')).split('\n')
            new_ls = []
            for new in vs:
                new = normalize_html_text(new)
                if len(new)>0 and new != key and new != '展开' and new != '收起':
                    new_ls.append(new)
            if key != '':
                info = Info(key=key, values=new_ls)
                info_ls.append(info)
        return info_ls
    
    def _get_item_image(self, driver) -> List[Image]:
        """获取该词条相关的图片
        """
        img_ls = driver.find_elements(by=By.CLASS_NAME, value='lazy-img')
        images = []
        for img in img_ls:
            src: str = img.get_attribute('data-src')
            alt: str = img.get_attribute('alt')
            if alt is not None and src is not None:
                if src.startswith('http') or src.startswith('https'):
                    item_name = self._get_item_name(driver=driver)
                    if item_name in alt:
                        images.append(Image(src=src, tag=alt))
        return images
    
    def _parse_item(self, driver):
        item_name = self._get_item_name(driver=driver)
        item_summary = self._get_item_summary(driver=driver)
        item_desc = self._get_item_desc(driver=driver)
        item_synonyms = self._get_item_synonyms(driver=driver)
        item_info = self._get_item_info(driver=driver)
        images = self._get_item_image(driver=driver)
        return Item(name=item_name, summary=item_summary, desc=item_desc, synonyms=item_synonyms, infos=item_info, images=images)
    
    def _get_search_url(self, search_text) -> str:
        return self.search_base_url + search_text
    
    @validate_arguments
    def search_items(self, search_text: str, num_return_items: conint(gt=0, le=10) = 1, headless: bool = True) -> List[Item]:
        """根据搜索的内容自动搜索百科条目

        Args:
            search_text (str): 带搜索的文本
            num_return_items (int, optional): 返回的搜索的条目. Defaults to 1.

        Returns:
            List[Item]: 所有返回条目
        """
        driver = self.driver
        items = []
        url = self._get_search_url(search_text=search_text)
        driver.get(url=url)
        results = driver.find_elements(by=By.CLASS_NAME, value='result-title')
        num_return_items = min(len(results), num_return_items)
        for res in results[:num_return_items]:
            res.click()
            driver.switch_to.window(driver.window_handles[1])
            scroll_to_bottom(driver=driver)
            item = self._parse_item(driver=driver)
            item.url = driver.current_url
            items.append(item)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        driver.quit()
        return items
    
    
class BaiduZhidao:
    def __init__(self, headless: bool = False) -> None:
        super().__init__()
        self.headers = { 'cookie': self._get_cookie(),
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36' }
        self.driver = get_driver(headless=headless)

    def _get_cookie(self) -> str:
        """首次访问百度知道获取cookie
        """
        r = requests.get('https://zhidao.baidu.com/')
        cookie_text = r.headers['Set-Cookie']
        span = re.search('BAIDUID=.{37}', cookie_text).span() # 百度知道的cookie位37位字符
        start = span[0] + len('BAIDUID=')
        end = span[1]
        cookie = cookie_text[start: end]
        return cookie
    
    
    def _get_searched_question_urls(self, query: str, max_questions: int= 10) -> List[str]:
        """通过搜索获取问答的地址
        - query: 带搜索的问题
        - max_questions: 最大问答数
        """
        urls = []
        max_page = (max_questions // 10) + 1
        for i in range(0, max_page):
            s_url = f'https://zhidao.baidu.com/search?word={query}&pn={i}'
            html = self._get_searched_html(url=s_url)
            if len(urls) >= max_questions:
                break
            for e in html.xpath('//dt[contains(@alog-alias, "result-title")]'):
                a = e.xpath('.//a')[0]
                url: str = a.get('href')
                if len(urls) < max_questions:
                    if url is not None:
                        if not url.startswith('https'):
                            url = 'https' + url[4:] # 改为https
                        urls.append(url)
                else:
                    break
                
        return urls
            
    
    @validate_arguments
    def search_questions(self, query: str, num_return_questions: conint(le=10, gt=0) = 1) -> List[Question]:
        """搜索查询问题,返回Question对象

        Args:
            query (str): 查询问题
            max_return_questions (int, optional): 最大返回问题数量. Defaults to 10.

        Returns:
            List[Question]: 所有查询到的相关问题
        """
        # 初始化浏览器
        driver = self.driver
        driver.implicitly_wait(5)
        # 转到百度知道网页并且搜索query
        driver.get('https://zhidao.baidu.com/')
        bar = driver.find_element(by=By.CLASS_NAME, value='hdi')
        bar.send_keys(query)
        search_btn = driver.find_element(by=By.ID, value='search-btn')
        search_btn.click()
        # 找到所有搜索结果
        results = driver.find_elements(by=By.CLASS_NAME, value='dt.mb-3.line')
        questions = []
        # 循环点击每个链接，并找到第一个答案
        for res in results[:num_return_questions]:
            res.find_element(by=By.CLASS_NAME, value='ti').click()
            driver.switch_to.window(driver.window_handles[1])
            scroll_to_bottom(driver=driver)
            c_ls = driver.find_elements(by=By.XPATH, value='//*[@id="wgt-ask"]/div[1]/span[2]')
            if len(c_ls)==0:
                content_result = driver.find_elements(by=By.CLASS_NAME, value='top-name-content')
                if len(content_result)>0:
                    content = content_result[0].text
                else:
                    content = ''
            else:
                content = c_ls[0].text
            title = driver.find_element(by=By.CLASS_NAME, value='ask-title').text
            answers = driver.find_elements(by=By.CLASS_NAME, value='rich-content-container.rich-text-')
            if len(answers) == 0:
                answers = driver.find_elements(by=By.CLASS_NAME, value='knowledge-content')
            answers = [a.text for a in answers if len(a.text) > 0]
            url = driver.current_url
            q = Question(url=url, content=content, title=title, answers=answers)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            questions.append(q)
        return questions
    
class SogouWechat:
    """通过搜狗微信搜索微信公众号的相关文章
    """
    def __init__(self, file_save_path : str, headless: bool = False) -> None:
        """
        Args:
            file_save_path (str): 文件保存文件夹，需要为绝对路径。
        """
        save_path = Path(file_save_path)
        if not save_path.exists():
            log.warning(f'路径不存在，路径已创建：{save_path}')
            save_path.mkdir()
        self.driver = get_driver(headless=headless, save_path=file_save_path)
        
    
    @validate_arguments     
    def search_article_to_pdf(self, query: str, num_articles: conint(gt=0, le=10) = 1) -> None:
        """搜索微信公众号文章,并保存为pdf.
        参数：
        - query: 搜索的相关公众号文章。
        - num_articles: 保存文章的数量,目前最多为10。
        """

        # 打开搜狗微信搜索
        self.driver.get("https://weixin.sogou.com/")
        self.driver.implicitly_wait(10)
        # 找到搜索栏，并添加搜索内容
        q = self.driver.find_element(by=By.NAME, value='query')
        q.send_keys(query)
        # 点击搜索
        self.driver.find_element(by=By.XPATH, value='//input[@uigs="search_article"]').click()
        for i in range(num_articles):
            # 点击对应的文章链接
            self.driver.find_element(by=By.XPATH, value=f'//a[@uigs="article_title_{i}"]').click()
            # 找到文章标题
            title = self.driver.find_element(by=By.XPATH, value=f'//a[@uigs="article_title_{i}"]').text.replace(" ","-") 
            # 切换窗口
            self.driver.switch_to.window(self.driver.window_handles[1])
            # 滑动到文章最下面，方便图片加载
            scroll_to_bottom(self.driver)
            # 下载pdf
            self.driver.execute_script('document.title="{}";window.print();'.format(title))
            # 关闭文章，并转到搜索窗口
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])