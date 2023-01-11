from django.core import mail

from w.services.technical.mail_service import EmailService
from w.tests.mixins.testcase_mixin import TestCaseMixin
from w.tests.serializers.serpy_serializers import MailOutboxSerializer


class TestEmailService(TestCaseMixin):

    # noinspection PyMethodMayBeStatic
    def setup_method(self, method):
        """clear mail outbox"""
        mail.outbox = []

    """
    send
    """

    def test_send_with_simple_email_return_int(self):
        """
        Ensure txt email sent succeed
        """
        params = {
            "recipients": "to@user.mail",
            "subject": "a mail subject",
            "message": "a mail content",
            "from_email": "from@user.com",
        }
        assert 1 == EmailService.send(**params)
        self.assert_equals_resultset(MailOutboxSerializer(mail.outbox[0]).data)

    def test_send_with_complex_email_return_int(self):
        """
        Ensure complex email (rendered via template) sent succeed
        """
        params = {
            "recipients": {
                "to": ["user1@to.com", "user2@to.com"],
                "bcc": "user1@bcc.com",
                "cc": ["user21@cc.com", "user22@cc.com"],
            },
            "subject": {
                "template_name": "email/email_subject.txt",
                "context": {"params1": "valueOne", "params2": "valueTwo"},
            },
            "message": {
                "template_name": "email/email_message.txt",
                "context": {"params1": "value11", "params2": "value22"},
            },
            "reply_to": "noreply@from.com",
        }
        assert 1 == EmailService.send(**params)
        self.assert_equals_resultset(MailOutboxSerializer(mail.outbox[0]).data)

    def test_send_with_html_email_return_int(self):
        """
        Ensure html email sent succeed
        """
        params = {
            "recipients": "to@user.mail",
            "subject": "a html email",
            "message": {
                "template_name": "email/email_message.html",
                "context": {"params1": "value11", "params2": "value22"},
            },
            "from_email": "from@user.com",
        }
        assert 1 == EmailService.send(**params)
        self.assert_equals_resultset(MailOutboxSerializer(mail.outbox[0]).data)

    """
    send_mass_mail
    """

    def test_send_mass_mail_with_simple_email_return_int(self):
        """
        Ensure txt email sent succeed
        """
        params = [
            ("to@user.mail", "a mail subject", "a mail content", {}),
            ("toto@user.mail", "another mail subject", "another mail content", {}),
        ]
        assert 2 == EmailService.send_mass_mail(params)
        self.assert_equals_resultset(MailOutboxSerializer(mail.outbox[0]).data)

    def test_send_mass_mail_with_complex_email_return_int(self):
        """
        Ensure complex email (rendered via template) sent succeed
        """
        params = [
            (
                {
                    "to": ["user1@to.com", "user2@to.com"],
                    "bcc": "user1@bcc.com",
                    "cc": ["user21@cc.com", "user22@cc.com"],
                },
                {
                    "template_name": "email/email_subject.txt",
                    "context": {"params1": "valueOne", "params2": "valueTwo"},
                },
                {
                    "template_name": "email/email_message.txt",
                    "context": {"params1": "value11", "params2": "value22"},
                },
                {
                    "reply_to": "noreply@from.com",
                    "attach_files": [self.get_datasets_dir("csv/simple.csv")],
                },
            )
        ]
        assert 1 == EmailService.send_mass_mail(params)
        self.assert_equals_resultset(MailOutboxSerializer(mail.outbox[0]).data)
