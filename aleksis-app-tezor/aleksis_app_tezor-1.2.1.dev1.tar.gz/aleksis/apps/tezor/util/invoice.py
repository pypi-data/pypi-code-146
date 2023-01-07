_provider_cache = {}


def provider_factory(variant, payment=None):
    from djp_sepa.providers import DirectDebitProvider, PaymentPledgeProvider  # noqa
    from payments.paypal import PaypalProvider  # noqa
    from payments.sofort import SofortProvider  # noqa

    if not payment:
        raise KeyError("Could not configure payment provider without a payment.")
    if not payment.group:
        raise KeyError(
            "Could not configure payment provider for a payment without an invoice group."
        )
    if not payment.group.client:
        raise KeyError(
            "Could not configure payment provider for an invoice group without a client."
        )

    cache_key = (variant, payment.group.client.pk)

    if cache_key in _provider_cache:
        return _provider_cache[cache_key]

    client = payment.group.client
    provider = None

    if variant == "sofort" and client.sofort_enabled:
        provider = SofortProvider(
            key=client.sofort_api_key, id=client.sofort_api_id, project_id=client.sofort_project_id
        )

    if variant == "paypal" and client.paypal_enabled:
        provider = PaypalProvider(
            client_id=client.paypal_client_id,
            secret=client.paypal_secret,
            capture=client.paypal_capture,
            endpoint="https://api.paypal.com",
        )

    if variant == "pledge" and client.pledge_enabled:
        provider = PaymentPledgeProvider()

    if variant == "sdd" and client.sdd_enabled:
        provider = DirectDebitProvider(
            creditor=client.sdd_creditor,
            creditor_identifier=client.sdd_creditor_identifier,
            iban=client.sdd_iban,
            bic=client.sdd_bic,
        )

    if provider is None:
        raise KeyError("Provider not found or not configured for client.")

    _provider_cache[cache_key] = provider
    return provider
