from w.django.tests.django_testcase import DjangoTestCase
from w.services.technical.template_service import TemplateService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestTemplateService(DjangoTestCase, TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()

    def test_render_template_with_success_returns_string(self):
        self.assert_equals_resultset(
            TemplateService.render_template(
                "email/email_message.html", context={"params1": "params1_value"}
            )
        )
