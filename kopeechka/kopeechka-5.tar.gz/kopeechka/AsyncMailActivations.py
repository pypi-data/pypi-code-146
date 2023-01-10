from kopeechka.errors import BAD_TOKEN
from kopeechka.async_methods import user_balance, mailbox_cancel, mailbox_get_email, mailbox_get_message, mailbox_get_bulk, mailbox_set_comment, mailbox_reorder, mailbox_get_fresh_id, mailbox_zones, mailbox_get_domains
from kopeechka.methods import user_balance as usr_balance


class AsyncMailActivations():
    def __init__(self, token: str):
        if not token:
            raise BAD_TOKEN
        self.check_token(token)
        self.token = token

    def check_token(self, token):
        try:
            usr_balance(token)
        except:
            raise BAD_TOKEN

    async def user_balance(self):
        return await user_balance(self.token)

    async def mailbox_get_email(self, site: str = None, mail_type: str = None, sender: str = None, regex: str = None,
                          soft_id: int = None, investor: int = None,
                          subject: str = None, clear: int = None):
        return await mailbox_get_email(self.token, site, mail_type, sender, regex, soft_id, investor, subject, clear)

    async def mailbox_get_message(self, full: int = None, id: int = None):
        return await mailbox_get_message(self.token, full, id)

    async def mailbox_cancel(self, id: int = None):
        return await mailbox_cancel(self.token, id)

    async def mailbox_reorder(self, site: str = None, email: str = None, regex: str = None, subject: str = None):
        return await mailbox_reorder(self.token, site, email, regex, subject)

    async def mailbox_get_bulk(self, count: int = None, comment: str = None, email: str = None, site: str = None):
        return await mailbox_get_bulk(self.token, count, comment, email, site)

    async def mailbox_set_comment(self, id: int = None, comment: str = None):
        return await mailbox_set_comment(self.token, id, comment)

    async def mailbox_get_fresh_id(self, site: str = None, email: str = None):
        return await mailbox_get_fresh_id(self.token, site, email)

    async def mailbox_get_domains(self, site: str = None):
        return await mailbox_get_domains(self.token, site)

    async def mailbox_zones(self, popular: int = None, zones: int = None):
        return await mailbox_zones(popular, zones)