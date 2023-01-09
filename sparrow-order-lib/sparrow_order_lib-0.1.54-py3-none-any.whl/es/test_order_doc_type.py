import unittest

from sparrow_order_lib.es import ESDoor
from sparrow_order_lib.es.constants import DocType
from sparrow_order_lib.es.es_util.client import init_es


class TestOrderDocType(unittest.TestCase):

    def setUp(self):
        MockData().index_mock_data()

    def tearDown(self):
        MockData().delete_mock_data()

    def test_order_data(self):
        '''  '''
        door = ESDoor(
            DocType.ORDER,
            id=MockData.mock_order_id,
            phone=MockData.mock_user_username
        )
        res = door.main()
        print(res)


class MockData(object):

    mock_order_id = 0
    mock_distribute_id = '1783adaaa3ac4c618fe735006f32081d'
    mock_user_id = '1783a65aa3ac4c618fe735xx6f32081d'
    mock_user_name = '卡卡西'
    mock_user_username = '13512341234'

    mock_data = {
        'id': mock_order_id,
        'aftersale_status': 'done',
        'assign_status': 'completed',
        # 'completed_time': null
        'created_time': "2022-03-11T16:08:58.712557",
        # 'delivertime_status': null,
        'distributes': [
            {
                "created_time": "2022-03-11T16:09:11.004717",
                "completed": "2022-03-11T16:10:11.730537",
                "id": mock_distribute_id,
                "number": "220311160911-125738",
                "order_id": mock_order_id,
                "distribute_status": "haitao_return",
            }
        ],
        'has_valid_to_assign': 0,
        'has_valid_to_shipping': 0,
        "number": "22031199900000008",
        'order_type': "haitao",
        'pay_method': 'once',
        'pay_status': 'finished',
        "shipping_address": {
            "id": 0,
            "name": "mmm",
            "phone": mock_user_username,
        },
        "shipping_method": "express",
        "shipping_status": "init",
        "sync_status": 1,
        "sync_time": "2022-03-11T16:09:10.656545",
        "updated_time": "2022-03-11T16:09:12.120511",
        "user_id": mock_user_id,
        "user": {
            "id": mock_user_id,
            "name": mock_user_name,
            "user_name": mock_user_username,
        },
        'lines': [
            {
                "barcode": "858991004923",
                "brand_id": 2069,
                # "gift": null,
                # "gift_id": null,
                # "giftproduct_id": null,
                "hg_code": "18061010005",
                "id": 524046,
                "if_gift": 0,
                "offer": "1",
                "order_id": mock_order_id,
                "product_id": 482639,
                "productmain_id": "90824",
                "shop_id": 1158,
                "shop_num": "217002",
                "shop_sku": "858991004923",
                "title": "LED太阳光台灯无影手术灯反射技术无频闪学生台灯",
            }
        ]
    }

    def index_mock_data(self):
        ''' 测试之前添加一条假数据 '''
        es = init_es()
        es.index(index=DocType.ORDER, body=self.mock_data)

    def delete_mock_data(self):
        ''' 删除假数据 '''
        es = init_es()

        body = {
            'query': {
                'must': [
                    {
                        'term': {'id': self.mock_order_id}
                    },
                    {
                        'term': {'distributes.id': self.mock_distribute_id}
                    }
                ]
            }
        }

        es.delete(index=DocType.ORDER, body=body)
