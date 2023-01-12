import qrunner
from qrunner import file_data


class TestClass(qrunner.TestCase):
    """pc首页"""

    @file_data('card_type', 'data.json')
    def test_getToolCardListForPc(self, card_type):
        """首页金刚位"""
        path = '/api/qzd-bff-app/qzd/v1/home/getToolCardListForPc'
        payload = {"type": card_type}
        self.post(path, json=payload)
        self.assertEq('code', 0)


if __name__ == '__main__':
    qrunner.main(
        platform='api',
        base_url='https://www.qizhidao.com'
    )
