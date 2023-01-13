from exactonline.rawapi import ExactRawApi

from exactonline.api.autorefresh import Autorefresh
from exactonline.api.unwrap import Unwrap
from exactonline.api.v1division import V1Division

from exactonline.api.bankaccounts import BankAccounts
from exactonline.api.contacts import Contacts
from exactonline.api.invoices import Invoices
from exactonline.api.ledgeraccounts import LedgerAccounts
from exactonline.api.quotations import Quotations
from exactonline.api.receivables import Receivables
from exactonline.api.relations import Relations
from exactonline.api.vatcodes import VatCodes

from tap_exactonline.helpers.secretsManager import update_secret


class ModifiedExactRawAPI(ExactRawApi):
    def refresh_token(self):
        ExactRawApi.refresh_token(self)
        secret = update_secret(
            self.storage.get('application','secret_id'),
            self.storage.get('transient', 'access_token'),
            self.storage.get('transient', 'refresh_token'),
            str(self.storage.get('transient', 'access_expiry'))
        )


class ExactWrapperApi(
    # Talk to /api/v1/{division} directly.
    V1Division,
    # Strip the surrounding "d" and "results" dictionary
    # items.
    Unwrap,
    # Ensure that tokens are refreshed in a timely manner.
    Autorefresh,
    # The base class comes last: talk to /api.
    ModifiedExactRawAPI
):
    bankaccounts = BankAccounts.as_property()
    contacts = Contacts.as_property()
    invoices = Invoices.as_property()
    ledgeraccounts = LedgerAccounts.as_property()
    quotations = Quotations.as_property()
    receivables = Receivables.as_property()
    relations = Relations.as_property()
    vatcodes = VatCodes.as_property()
