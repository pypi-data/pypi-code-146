import qrunner


class TestGetToolCardListForPc(qrunner.TestCase):
    """pc首页金刚位"""

    def test_getToolCardListForPc(self):
        """type=1"""
        path = '/api/qzd-bff-app/qzd/v1/home/getToolCardListForPc'
        payload = {"type": 1}
        self.post(path, json=payload)
        self.assert_eq('code', 0)


if __name__ == '__main__':
    qrunner.main(
        platform='api',
        base_url='https://www.qizhidao.com'
    )
