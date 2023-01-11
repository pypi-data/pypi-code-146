import qrunner
from qrunner import story, title


class HomePage(qrunner.Page):
    LOC_AD_CLOSE = {'label': 'close white big', 'desc': '首页广告关闭按钮'}
    LOC_MY = {'label': '我的', 'desc': '首页底部我的入口'}
    
    def go_my(self):
        self.elem(**self.LOC_AD_CLOSE).click()
        self.elem(**self.LOC_MY).click()


@story('首页')
class TestClass(qrunner.TestCase):

    def start(self):
        self.hp = HomePage(self.driver)
        self.elem_close = self.elem(label='close white big', desc='首页广告关闭按钮')
        self.elem_my = self.elem(label='我的', desc='首页底部我的入口')

    @title('pom模式用例')
    def test_pom(self):
        self.start_app()
        self.hp.go_my()
        self.assertText('我的订单')
        self.stop_app()

    @title('普通模式用例')
    def test_normal(self):
        self.start_app()
        self.elem_close.click()
        self.elem_my.click()
        self.assertText('我的订单')
        self.stop_app()


if __name__ == '__main__':
    qrunner.main(
        platform='ios',
        device_id='00008101-000E646A3C29003A',
        pkg_name='com.qizhidao.company'
    )
