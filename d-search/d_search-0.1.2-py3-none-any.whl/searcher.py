import requests
from pydantic import BaseModel, constr, HttpUrl, conint
from typing import List
from .utils import normalize_html_text
from pathlib import Path
import re
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import json
import time


class Info(BaseModel):
    key: str
    values: List[str]
    
    
class Image(BaseModel):
    src: str
    tag: str
    
    def _download(self) -> bytes:
        res = requests.get(url=self.src)
        return res.content
    
    def save(self, file_path: Path):
        with open(file_path, 'wb') as f:
            f.write(self._download())


class Item(BaseModel):
    """百科的一个条目
    - name: 词条名称
    - desc: 词条描述,用于混淆词条
    - summary: 词条摘要
    - synonym: 同义词
    """
    url: HttpUrl = ''
    name: constr(strip_whitespace=True)
    desc: constr(strip_whitespace=True)
    summary: constr(strip_whitespace=True)
    synonyms: List[constr(strip_whitespace=True, min_length=1)]
    information: List[Info] = []
    images: List[Image] = []


class BaiduPedia:
    """百度百科
    """
    item_base_url = "https://baike.baidu.com/item/"
    search_base_url = 'https://baike.baidu.com/search?word='
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36' }        

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
    
    def _parse_item_html(self, driver):
        item_name = self._get_item_name(driver=driver)
        item_summary = self._get_item_summary(driver=driver)
        item_desc = self._get_item_desc(driver=driver)
        item_synonyms = self._get_item_synonyms(driver=driver)
        item_info = self._get_item_info(driver=driver)
        images = self._get_item_image(driver=driver)
        return Item(name=item_name, summary=item_summary, desc=item_desc, synonyms=item_synonyms, information=item_info, images=images)
    
    def _get_search_url(self, search_text) -> str:
        return self.search_base_url + search_text
    
    def search_items(self, search_text: str, num_return_items: conint(gt=0, le=10) = 1) -> List[Item]:
        """根据搜索的内容自动搜索百科条目

        Args:
            search_text (str): 带搜索的文本
            num_return_items (int, optional): 返回的搜索的条目. Defaults to 1.

        Returns:
            List[Item]: 所有返回条目
        """
        driver = Chrome()
        items = []
        url = self._get_search_url(search_text=search_text)
        driver.get(url=url)
        results = driver.find_elements(by=By.CLASS_NAME, value='result-title')
        num_return_items = min(len(results), num_return_items)
        for res in results[:num_return_items]:
            res.click()
            driver.switch_to.window(driver.window_handles[1])
            item = self._parse_item_html(driver=driver)
            item.url = driver.current_url
            items.append(item)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        driver.quit()
        return items
    
class Answer(BaseModel):
    text: constr(strip_whitespace=True, min_length=1)   
    
class Question(BaseModel):
    url: str
    title: constr(strip_whitespace=True, min_length=1)
    content: constr(strip_whitespace=True, min_length=0)
    answers: List[Answer]
    
    
class BaiduZhidao:
    def __init__(self) -> None:
        super().__init__()
        self.headers = { 'cookie': self._get_cookie(),
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36' }

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
            
    def _parse_question_url(self, url) -> Question:
        """将搜索得到的问题的url解析为question对象
        """
        res = requests.get(url=url, headers=self.headers)
        res.encoding = 'gbk'
        html = HTML(res.text)
        title = html.xpath('//span[@class="ask-title"]/text()')[0]
        contents = html.xpath('//div[@class="line mt-5 q-content"]/span[@class="con-all"]/text()')
        content = ''.join(contents).strip()
        ans_eles = html.xpath('//div[@class="rich-content-container rich-text-"]')
        answers = []
        for ans in ans_eles:
            ans_text = ''.join(ans.xpath('.//text()')).strip()
            ans_text = normalize_html_text(ans_text)
            answer = Answer(text=ans_text)
            if answer not in answers:
                answers.append(answer)
        ques = Question(title=title, content=content, answers=answers, url=url)
        return ques
    
    def search_questions(self, query: str, num_return_questions: int = 10) -> List[Question]:
        """搜索查询问题,返回Question对象

        Args:
            query (str): 查询问题
            max_return_questions (int, optional): 最大返回问题数量. Defaults to 10.

        Returns:
            List[Question]: 所有查询到的相关问题
        """
        questions = []
        urls = self._get_searched_question_urls(query=query, max_questions=num_return_questions)
        for url in urls:
            try:
                ques = self._parse_question_url(url=url)
                questions.append(ques)
            except Exception as e:
                pass
        return questions
    
class SogouWechat:
    
    def _scroll_to_bottom(self, driver):
        """将公众号文章一点一点滑动到底部，方便加载图片
        """
        js = "return action=document.body.scrollHeight"
        # 初始化现在滚动条所在高度为0
        height = 0
        # 当前窗口总高度
        new_height = driver.execute_script(js)

        while height < new_height:
            # 将滚动条调整至页面底部
            for i in range(height, new_height, 100):
                driver.execute_script('window.scrollTo(0, {})'.format(i))
                time.sleep(0.5)
            height = new_height
            new_height = driver.execute_script(js)
            
    def search_article(self, query: str, pdf_save_path: Path, num_articles: conint(gt=0, le=10) = 1):
        appState = """{"recentDestinations": [{"id": "Save as PDF","origin": "local"}],"mediaSize": {"height_microns": 279400,"name": "NA_LETTER","width_microns": 215900,"custom_display_name": "Letter"},"selectedDestinationId": "Save as PDF","version": 2,"isHeaderFooterEnabled": false}"""
        appState = json.loads(appState)
        profile = {'printing.print_preview_sticky_settings.appState': json.dumps(appState),'savefile.default_directory': pdf_save_path,'download.default_directory': pdf_save_path}
        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option('prefs', profile)
        # 该参数必须存在，不设置会无法使用打印，保存全屏图片等功能
        chrome_options.add_argument('--kiosk-printing')
        # 用指定路径的ChromeDriver驱动去打开一个浏览器窗口
        driver = Chrome(options=chrome_options)

        # 打开搜狗微信搜索
        driver.get("https://weixin.sogou.com/")
        # 找到搜索栏，并添加搜索内容
        q = driver.find_element(by=By.NAME, value='query')
        q.send_keys(query)
        # 点击搜索
        driver.find_element(by=By.XPATH, value='//input[@uigs="search_article"]').click()
        for i in range(num_articles):
            # 点击对应的文章链接
            driver.find_element(by=By.XPATH, value=f'//a[@uigs="article_title_{i}"]').click()
            # 找到文章标题
            title = driver.find_element(by=By.XPATH, value=f'//a[@uigs="article_title_{i}"]').text.replace(" ","-") 
            # 切换窗口
            driver.switch_to.window(driver.window_handles[1])
            # 滑动到文章最下面，方便图片加载
            time.sleep(2)
            self._scroll_to_bottom(driver)
            # 下载pdf
            driver.execute_script('document.title="{}";window.print();'.format(title))
            time.sleep(2)
            # 关闭文章，并转到搜索窗口
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        driver.quit()