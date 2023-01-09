import qrunner
from qrunner import Elem


class PatentPage(qrunner.Page):
    """查专利首页"""
    search_input = Elem(id_='driver-home-step1', desc='查专利首页输入框')
    search_submit = Elem(id_='driver-home-step2', desc='查专利首页搜索确认按钮')
    
    def simple_search(self, keyword: str):
        """简单搜索"""
        self.elem(self.search_input).set_text(keyword)
        self.elem(self.search_submit).click()


class TestPatentSearch(qrunner.TestCase):
    """搜索无人机"""

    def start(self):
        """页面和元素初始化"""
        self.pp = PatentPage(self.driver)

    def test_pom(self):
        """pom模式代码"""
        self.driver.open_url()
        self.pp.simple_search('无人机')
        self.assert_in_page('王刚毅')


if __name__ == '__main__':
    qrunner.main(
        platform='web',
        base_url='https://patents.qizhidao.com/'
    )
