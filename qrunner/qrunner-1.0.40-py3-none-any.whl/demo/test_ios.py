import qrunner
from qrunner import Elem


class HomePage(qrunner.Page):
    """APP首页"""
    ad_close = Elem(label='close white big', desc='广告关闭按钮')
    search_entry = Elem(xpath='//*[@label="空列表"]/Other[2]', desc='搜索入口')
    
    def go_search(self):
        """进入综合搜索"""
        self.elem(self.ad_close).click_exists()
        self.elem(self.search_entry).click()


class SearchPage(qrunner.Page):
    """综合搜索页"""
    search_input = Elem(class_name='TextField', desc='搜索框')
    search_confirm = Elem(class_name='StaticText', label='搜索', desc='搜索确认按钮')

    def search(self, keyword: str):
        """输入并搜索"""
        self.elem(self.search_input).set_text(keyword)
        self.elem(self.search_confirm).click()


class TestSearch(qrunner.TestCase):
    """搜索无人机"""

    def start(self):
        self.hp = HomePage(self.driver)
        self.sp = SearchPage(self.driver)

    def test_pom(self):
        self.hp.go_search()
        self.sp.search('无人机')
        self.assert_in_page('航天彩虹无人机股份有限公司')


if __name__ == '__main__':
    qrunner.main(
        platform='ios',
        device_id='00008101-000E646A3C29003A',
        pkg_name='com.qizhidao.company'
    )
