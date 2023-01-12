# -*- encoding: utf-8 -*-

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from magnet_data.currencies.enums import CurrencyAcronyms


class CurrencyValue(models.Model):
    """
    This model stores the value that the `base_currency` currency has as
    `counter_currency` currency on the `date`
    """

    value = models.DecimalField(
        _("value"),
        decimal_places=6,
        max_digits=20,
    )
    date = models.DateField(
        verbose_name=_("currency date"),
        db_index=True,
    )
    base_currency = models.CharField(
        _("base currency"),
        max_length=5,
        help_text=_("The acronym of the base currency"),
        choices=CurrencyAcronyms.django_model_choices,
    )
    counter_currency = models.CharField(
        _("counter currency"),
        max_length=5,
        help_text=_("The acronym of the counter currency"),
        choices=CurrencyAcronyms.django_model_choices,
    )

    class Meta:
        verbose_name = _("currency value")
        verbose_name_plural = _("currency values")
        unique_together = (("base_currency", "counter_currency", "date"),)
        ordering = ("date",)

    def __str__(self) -> str:
        return f"{self.base_currency}/{self.counter_currency}-{self.date}-{self.value}"
