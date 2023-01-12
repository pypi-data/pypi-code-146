import os

from . import resources
from .enums import Environment
from .exceptions import BelvoAPIException
from .http import APISession


class Client:
    def __init__(self, secret_key_id: str, secret_key_password: str, url: str = None) -> None:
        """# Connect to the Belvo API

        In order to use Belvo API, you will have to login into a new session by using
        a _secret key_.

        Secret keys are generated from the Belvo API dashboard. For more information, please visit
        [our Developers portal](https://developers.belvo.com/docs/get-your-belvo-api-keys)

        ### Method

        ```python
        def __init__(secret_key_id: str, secret_key_password: str, url: str = None) -> None:
            ...
        ```

        You **must** provide your `secret_key_id` and `secret_key_password`.

        The `url` tells the client to which Belvo API host should attempt to connect,
        this allows you to switch from a sandbox to a production environment.

        You can also set which Belvo API host to use, by setting the `BELVO_API_URL`
        environment variable.

        When creating a new instance of `Client`, it will automatically perform a login
        and create a `JWTSession` (if the credentials are valid).


        ### Example
        ```python
        # Creating a client instance to connect to Belvo API
        from belvo.client import Client

        my_client = Client(
            "your-secret-key-id",
            "your-secret-key-password",
            "https://api.belvo.com"
        )


        # Creating a client that takes url from the environment.
        # We assume that you have set BELVO_API_URL before
        # (e.g. export BELVO_API_URL=https://sandbox.belvo.com
        my_client = Client(
            "your-secret-key-id",
            "your-secret-key-password"
        )
        ```

        ## Nested resources

        All resources in the Belvo API are nested attributes in your client instance,
        these resources are available **only** if you provide valid credentials.

        Args:
            secret_key_id (str): Your Belvo secret ID.
            secret_key_password (str): Your Belvo secret password.
            url (str, optional): The URL of the environment you want to connect to.

        Raises:
            BelvoAPIException
        """
        if url is None:
            url = os.getenv("BELVO_API_URL")

        url = Environment.get_url(url)
        if not url:
            raise BelvoAPIException("You need to provide a URL or a valid environment.")

        self.session = APISession(url)

        if not self.session.login(secret_key_id, secret_key_password):
            raise BelvoAPIException("Login failed.")

        self._links = resources.Links(self.session)
        self._accounts = resources.Accounts(self.session)
        self._transactions = resources.Transactions(self.session)
        self._balances = resources.Balances(self.session)
        self._institutions = resources.Institutions(self.session)
        self._incomes = resources.Incomes(self.session)
        self._owners = resources.Owners(self.session)
        self._invoices = resources.Invoices(self.session)
        self._recurring_expenses = resources.RecurringExpenses(self.session)
        self._risk_insights = resources.RiskInsights(self.session)
        self._tax_returns = resources.TaxReturns(self.session)
        self._tax_declarations = resources.TaxDeclarations(self.session)
        self._tax_status = resources.TaxStatus(self.session)
        self._tax_compliance_status = resources.TaxComplianceStatus(self.session)
        self._tax_retentions = resources.TaxRetentions(self.session)
        self._statements = resources.Statements(self.session)
        self._widget_token = resources.WidgetToken(self.session)
        self._investments_portfolios = resources.InvestmentsPortfolios(self.session)

    @property
    def Links(self):
        return self._links

    @property
    def Accounts(self):
        return self._accounts

    @property
    def Transactions(self):
        return self._transactions

    @property
    def Balances(self):
        return self._balances

    @property
    def Institutions(self):
        return self._institutions

    @property
    def Incomes(self):
        return self._incomes

    @property
    def Owners(self):
        return self._owners

    @property
    def Invoices(self):
        return self._invoices

    @property
    def RecurringExpenses(self):
        return self._recurring_expenses

    @property
    def RiskInsights(self):
        return self._risk_insights

    @property
    def TaxReturns(self):
        return self._tax_returns

    @property
    def TaxDeclarations(self):
        return self._tax_declarations

    @property
    def TaxComplianceStatus(self):
        return self._tax_compliance_status

    @property
    def TaxStatus(self):
        return self._tax_status

    @property
    def TaxRetentions(self):
        return self._tax_retentions

    @property
    def Statements(self):
        return self._statements

    @property
    def WidgetToken(self):
        return self._widget_token

    @property
    def InvestmentsPortfolios(self):
        return self._investments_portfolios
