from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from localflavor.generic.models import BICField, IBANField

from aleksis.core.mixins import ExtensibleModel


class Client(ExtensibleModel):
    VARIANT_DISPLAY = {
        "paypal": (_("PayPal"), "logos:paypal"),
        "sofort": (_("Klarna / Sofort"), "simple-icons:klarna"),
        "pledge": (_("Payment pledge / manual payment"), "mdi:hand-coin"),
        "sdd": (_("SEPA Direct Debit"), "mdi:bank-transfer"),
    }
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    email = models.EmailField(verbose_name=_("Email"))

    sofort_enabled = models.BooleanField(verbose_name=_("Sofort / Klarna enabled"), default=False)
    sofort_api_id = models.CharField(
        verbose_name=_("Sofort / Klarna API ID"), blank=True, max_length=255
    )
    sofort_api_key = models.CharField(
        verbose_name=_("Sofort / Klarna API key"), blank=True, max_length=255
    )
    sofort_project_id = models.CharField(
        verbose_name=_("Sofort / Klarna Project ID"), blank=True, max_length=255
    )

    paypal_enabled = models.BooleanField(verbose_name=_("PayPal enabled"), default=False)
    paypal_client_id = models.CharField(
        verbose_name=_("PayPal client ID"), blank=True, max_length=255
    )
    paypal_secret = models.CharField(verbose_name=_("PayPal secret"), blank=True, max_length=255)
    paypal_capture = models.BooleanField(
        verbose_name=_("Use PayPal Authorize & Capture"), default=False
    )

    sdd_enabled = models.BooleanField(verbose_name=_("Debit enabled"), default=False)
    sdd_creditor = models.CharField(
        verbose_name=_("SEPA Direct Debit - Creditor name"), blank=True, max_length=255
    )
    sdd_creditor_identifier = models.CharField(
        verbose_name=_("SEPA Direct Debit - Creditor identifier"),
        blank=True,
        max_length=35,
        validators=[RegexValidator("^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,31}$")],
    )
    sdd_iban = IBANField(verbose_name=_("IBAN of bank account"), blank=True)
    sdd_bic = BICField(verbose_name=_("BIC/SWIFT code of bank"), blank=True)

    pledge_enabled = models.BooleanField(verbose_name=_("Pledge enabled"), default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "site"], name="uniq_client_per_site"),
            models.CheckConstraint(
                check=(
                    (
                        Q(sofort_enabled=True)
                        & ~Q(sofort_api_id="")
                        & ~Q(sofort_api_key="")
                        & ~Q(sofort_project_id="")
                    )
                    | Q(sofort_enabled=False)
                ),
                name="sofort_enabled_configured",
            ),
            models.CheckConstraint(
                check=(
                    (
                        Q(sdd_enabled=True)
                        & ~Q(sdd_creditor="")
                        & ~Q(sdd_creditor_identifier="")
                        & ~Q(sdd_iban="")
                        & ~Q(sdd_bic="")
                    )
                    | Q(sdd_enabled=False)
                ),
                name="sdd_enabled_configured",
            ),
            models.CheckConstraint(
                check=(
                    (Q(paypal_enabled=True) & ~Q(paypal_client_id="") & ~Q(paypal_secret=""))
                    | Q(paypal_enabled=False)
                ),
                name="paypal_enabled_configured",
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def get_variant_choices(self=None):
        choices = []
        for variant in Client.VARIANT_DISPLAY.keys():
            if self and not getattr(self, f"{variant}_enabled"):
                continue
            choices.append((variant, Client.VARIANT_DISPLAY[variant][0]))
        return choices
