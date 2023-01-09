import aiohttpx

from typing import Optional, Dict, Callable

from aiolago.schemas import *
from aiolago.utils.config import settings

class ApiRoutes:

    """
    Container for all the routes in the API.
    """
    add_ons: AddOnRoute = None
    applied_add_ons: AppliedAddOnRoute = None
    applied_coupons: AppliedCouponRoute = None
    billable_metrics: BillableMetricRoute = None
    coupons: CouponRoute = None
    customers: CustomerRoute = None
    events: EventRoute = None
    invoices: InvoiceRoute = None
    organizations: OrganizationRoute = None
    plans: PlanRoute = None
    subscriptions: SubscriptionRoute = None
    wallets: WalletRoute = None
    wallet_transactions: WalletTransactionRoute = None
    webhooks: WebhookRoute = None

    def __init__(
        self,
        client: aiohttpx.Client,
        headers: Optional[Dict] = None,
        debug_enabled: Optional[bool] = False,
        on_error: Optional[Callable] = None,
        ignore_errors: Optional[bool] = False,
        timeout: Optional[int] = None,

        **kwargs
    ):
        self.client = client
        self.headers = headers or settings.get_headers()
        self.debug_enabled = debug_enabled
        self.on_error = on_error
        self.ignore_errors = ignore_errors

        self.kwargs = kwargs

        self.add_ons = AddOnRoute(client = client, headers = headers, debug_enabled = debug_enabled, on_error = on_error, ignore_errors = ignore_errors, timeout = timeout)
        self.applied_add_ons = AppliedAddOnRoute(client = client, headers = headers, debug_enabled = debug_enabled, on_error = on_error, ignore_errors = ignore_errors, timeout = timeout)
        self.applied_coupons = AppliedCouponRoute(client = client, headers = headers, debug_enabled = debug_enabled, on_error = on_error, ignore_errors = ignore_errors, timeout = timeout)
        self.billable_metrics = BillableMetricRoute(client = client, headers = headers, debug_enabled = debug_enabled, on_error = on_error, ignore_errors = ignore_errors, timeout = timeout)
        self.coupons = CouponRoute(client = client, headers = headers, debug_enabled = debug_enabled, on_error = on_error, ignore_errors = ignore_errors, timeout = timeout)
        self.customers = CustomerRoute(client = client, headers = headers, debug_enabled = debug_enabled, on_error = on_error, ignore_errors = ignore_errors, timeout = timeout)
        self.events = EventRoute(client = client, headers = headers, debug_enabled = debug_enabled, on_error = on_error, ignore_errors = ignore_errors, timeout = timeout)
        self.invoices = InvoiceRoute(client = client, headers = headers, debug_enabled = debug_enabled, on_error = on_error, ignore_errors = ignore_errors, timeout = timeout)
        self.organizations = OrganizationRoute(client = client, headers = headers, debug_enabled = debug_enabled, on_error = on_error, ignore_errors = ignore_errors, timeout = timeout)
        self.plans = PlanRoute(client = client, headers = headers, debug_enabled = debug_enabled, on_error = on_error, ignore_errors = ignore_errors, timeout = timeout)
        self.subscriptions = SubscriptionRoute(client = client, headers = headers, debug_enabled = debug_enabled, on_error = on_error, ignore_errors = ignore_errors, timeout = timeout)
        self.wallets = WalletRoute(client = client, headers = headers, debug_enabled = debug_enabled, on_error = on_error, ignore_errors = ignore_errors, timeout = timeout)
        self.wallet_transactions = WalletTransactionRoute(client = client, headers = headers, debug_enabled = debug_enabled, on_error = on_error, ignore_errors = ignore_errors, timeout = timeout)
        self.webhooks = WebhookRoute(client = client, headers = headers, debug_enabled = debug_enabled, on_error = on_error, ignore_errors = ignore_errors, timeout = timeout)




