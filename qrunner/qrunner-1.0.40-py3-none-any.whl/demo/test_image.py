import qrunner
from qrunner import Elem


class HomePage(qrunner.Page):
    """APP首页"""
    ad_close = Elem(label='close white big', desc='广告关闭按钮')
    patent_entry = Elem(text='查专利', desc='查专利入口')

    def go_patent(self):
        """进入查专利"""
        self.ios_elem(self.ad_close).click_exists()
        self.ios_elem(self.patent_entry).click()


class PatentSearch(qrunner.Page):
    """查专利"""
    report_entry = Elem(image='patent_report_entry.png', desc='分析报告')
    tech_report = Elem(image='patent_tech_entry.png', desc='技术全景报告入口')
    create_tech = Elem(image='patent_create_tech_title.png', desc='创建技术报告标题')

    def go_tech_report(self):
        self.image_elem(self.report_entry).click()
        self.image_elem(self.tech_report).click()
        assert self.image_elem(self.create_tech).exists()


class TestSearch(qrunner.TestCase):
    """搜索无人机"""

    def start(self):
        self.hp = HomePage(self.driver)
        self.ps = PatentSearch(self.driver)

    def test_pom(self):
        self.hp.go_patent()
        self.ps.go_tech_report()


if __name__ == '__main__':
    qrunner.main(
        platform='ios',
        device_id='00008101-000E646A3C29003A',
        pkg_name='com.qizhidao.company'
    )
