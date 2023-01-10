import unittest

from lumipy.query.expression.column.source_column import SourceColumn
from lumipy.test.unit.utilities.test_utils import make_test_atlas


class TestStrColumnGetters(unittest.TestCase):

    def setUp(self) -> None:
        self.atlas = make_test_atlas()
        self.ar = self.atlas.lusid_logs_apprequest()

    def test_str_accessor_get(self):

        attr = self.ar.request_id
        camel = self.ar['RequestId']
        snake = self.ar['request_id']

        self.assertIsInstance(camel, SourceColumn)
        self.assertIsInstance(snake, SourceColumn)

        self.assertEqual(hash(camel), hash(attr))
        self.assertEqual(hash(snake), hash(attr))

    def test_aliased_str_accessor_get(self):

        tv = self.ar.select(SecondsDuration=self.ar.duration*0.001).to_table_var()

        attr = tv.seconds_duration
        camel = tv['SecondsDuration']
        snake = tv['seconds_duration']

        self.assertEqual(hash(camel), hash(attr))
        self.assertEqual(hash(snake), hash(attr))

    def test_prefixed_str_accessor_get(self):

        ar = self.ar
        rt = self.atlas.lusid_logs_requesttrace()

        tv = ar.select(ar.method, ar.request_id).where(
            (ar.application == 'lusid')
            & (ar.event_type == 'Completed')
        ).limit(10).to_table_var()

        join = tv.left_join(rt, on=rt.request_id == tv.request_id)

        attr = join.function_name
        camel = join['FunctionName']
        snake = join['FunctionName']
        self.assertEqual(hash(camel), hash(attr))
        self.assertEqual(hash(snake), hash(attr))

        attr = join.request_id_lhs
        camel = join['RequestId_lhs']
        snake = join['request_id_lhs']
        self.assertEqual(hash(camel), hash(attr))
        self.assertEqual(hash(snake), hash(attr))

        q = join.select(tv['RequestId'], rt['FunctionName'], rt['SelfTime'])
        self.assertEqual(len(q.get_columns()), 3)

    def test_key_error_on_missing_col(self):
        with self.assertRaises(KeyError) as ke:
            c = self.ar['NotAColumn']
