from .common import JinsiTestCase


class JinsiMultipleInvocationsOnSameLevel(JinsiTestCase):

    def test_multiple_call_returning_lists(self):
        doc = """\
            ::let:
              template:
                - foo: <<$bar>>
                - some: thing
            key:
              ::call template:
                bar: 1337
              ::call template:
                bar: 4711
        """

        expected = {
            'key': [
                {
                    "foo": "1337"
                },
                {
                    "some": "thing"
                },
                {
                    "foo": "4711"
                },
                {
                    "some": "thing"
                },
            ]
        }

        self.check(expected, doc)
