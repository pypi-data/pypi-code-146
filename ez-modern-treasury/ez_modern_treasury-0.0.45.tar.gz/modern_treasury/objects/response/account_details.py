from ..shared import mask_number


class AccountDetailsResponse:
    def __init__(self, json):
        self.json = json

    @property
    def id(self):
        return self.json.get('id')

    @property
    def account_number(self):
        return self.json.get('account_number')

    @property
    def account_number_type(self):
        return self.json.get('account_number_type')

    @property
    def live_mode(self):
        return self.json.get('live_mode')

    def __str__(self) -> str:
        return (
            f"id: { self.id }, account_number: { mask_number(self.account_number) }, "
            f"account_number_type: { self.account_number_type }, live_mode: { self.live_mode }"
        )
