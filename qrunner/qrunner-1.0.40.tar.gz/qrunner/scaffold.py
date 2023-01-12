import os.path
import sys

run_content_android = """import qrunner


if __name__ == '__main__':
    qrunner.main(
        platform='android',
        device_id='UJK0220521066836',
        pkg_name='com.qizhidao.clientapp',
    )
"""

run_content_ios = """import qrunner


if __name__ == '__main__':
    qrunner.main(
        platform='ios',
        device_id='00008101-000E646A3C29003A',
        pkg_name='com.qizhidao.company'
    )
"""

run_content_web = """import qrunner


if __name__ == '__main__':
    qrunner.main(
        platform='web',
        base_url='https://www-pre.qizhidao.com',
    )
"""

run_content_api = """import qrunner


if __name__ == '__main__':
    qrunner.main(
        platform='api',
        base_url='https://www-pre.qizhidao.com',
    )
"""

case_content_android = """import qrunner
from qrunner import story, title


class HomePage(qrunner.Page):
    LOC_AD_CLOSE = {'id_': 'id/bottom_btn', 'desc': '首页广告关闭按钮'}
    LOC_MY = {'id_': 'id/bottom_view', 'index': 3, 'desc': '首页底部我的入口'}
    
    def go_my(self):
        self.elem(**self.LOC_AD_CLOSE).click()
        self.elem(**self.LOC_MY).click()


@story('首页')
class TestClass(qrunner.TestCase):
    
    def start(self):
        self.hp = HomePage(self.driver)
        self.elem_close = self.elem(id_='id/bottom_btn', desc='首页广告关闭按钮')
        self.elem_my = self.elem(id_='id/bottom_view', index=3, desc='首页底部我的入口')
    
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
        platform='android',
        device_id='UJK0220521066836',
        pkg_name='com.qizhidao.clientapp'
    )
"""

case_content_ios = """import qrunner
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
"""

case_content_web = """import qrunner
from qrunner import story, title


class PatentPage(qrunner.Page):
    url = None
    LOC_SEARCH_INPUT = {'id_': 'driver-home-step1', 'desc': '查专利首页输入框'}
    LOC_SEARCH_SUBMIT = {'id_': 'driver-home-step2', 'desc': '查专利首页搜索确认按钮'}
    
    def simple_search(self):
        self.elem(**self.LOC_SEARCH_INPUT).set_text('无人机')
        self.elem(**self.LOC_SEARCH_SUBMIT).click()


@story('专利检索')
class TestClass(qrunner.TestCase):
    
    def start(self):
        self.pp = PatentPage(self.driver)
        self.elem_input = self.elem(id_='driver-home-step1', desc='查专利首页输入框')
        self.elem_submit = self.elem(id_='driver-home-step2', desc='查专利首页搜索确认按钮')
    
    @title('pom模式代码')
    def test_pom(self):
        self.pp.open()
        self.pp.simple_search()
        self.assertTitle('无人机专利检索-企知道')
    
    @title('普通模式代码')
    def test_normal(self):
        self.open()
        self.elem_input.click()
        self.elem_submit.click()
        self.assertTitle('无人机专利检索-企知道')


if __name__ == '__main__':
    qrunner.main(
        platform='web',
        base_url='https://patents.qizhidao.com/'
    )
"""

case_content_api = """import qrunner
from qrunner import title, file_data, story


@story('PC站首页')
class TestClass(qrunner.TestCase):

    @title('查询PC站首页banner列表')
    @file_data('card_type', 'data.json')
    def test_getToolCardListForPc(self, card_type):
        path = '/api/qzd-bff-app/qzd/v1/home/getToolCardListForPc'
        payload = {"type": card_type}
        self.post(path, json=payload)
        self.assertEq('code', 0)


if __name__ == '__main__':
    qrunner.main(
        platform='api',
        base_url='https://www.qizhidao.com'
    )
"""

data_content = """{
  "card_type": [0, 1, 2]
}
"""


def create_scaffold(project_name, platform):
    """create scaffold with specified project name."""

    def create_folder(path):
        os.makedirs(path)
        msg = f"created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    create_folder(project_name)
    # 新增测试用例目录
    create_folder(os.path.join(project_name, "test_dir"))
    create_file(
        os.path.join(project_name, "test_dir", "__init__.py"),
        "",
    )
    # 新增测试数据目录
    create_folder(os.path.join(project_name, "test_data"))
    create_file(
        os.path.join(project_name, "test_data", "data.json"),
        data_content,
    )
    if platform == "android":
        # 新增框架入口程序
        create_file(
            os.path.join(project_name, "run.py"),
            run_content_android,
        )
        # 新增安卓测试用例
        create_file(
            os.path.join(project_name, "test_dir", "test_android.py"),
            case_content_android,
        )

    elif platform == "ios":
        # 新增框架入口程序
        create_file(
            os.path.join(project_name, "run.py"),
            run_content_ios,
        )
        # 新增ios测试用例
        create_file(
            os.path.join(project_name, "test_dir", "test_ios.py"),
            case_content_ios,
        )
    elif platform == "web":
        # 新增框架入口程序
        create_file(
            os.path.join(project_name, "run.py"),
            run_content_web,
        )
        # 新增web测试用例
        create_file(
            os.path.join(project_name, "test_dir", "test_web.py"),
            case_content_web,
        )
    elif platform == "api":
        # 新增框架入口程序
        create_file(
            os.path.join(project_name, "run.py"),
            run_content_api,
        )
        # 新增接口测试用例
        create_file(
            os.path.join(project_name, "test_dir", "test_api.py"),
            case_content_api,
        )
    else:
        print("请输入正确的平台: android、ios、web、api")
        sys.exit()
