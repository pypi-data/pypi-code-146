from django.db import models
from model_utils.models import TimeStampedModel

from b2_utils.fields import States

__all__ = [
    "Phone",
    "City",
    "Address",
]


class Phone(TimeStampedModel):
    """A TimeStampedModel Phone model, ordered by it's creation date"""

    country_code = models.CharField("Código do país", default="55", max_length=3)
    area_code = models.CharField("Código de Area", max_length=3)
    number = models.CharField("Número", max_length=9)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Telefone"
        verbose_name_plural = "Telefones"

    def __str__(self):
        return f"({self.country_code}) {self.area_code}-{self.number}"


class City(TimeStampedModel):
    """A TimeStampedModel City model, ordered by it's creation date"""

    name = models.CharField("Cidade", max_length=255)
    state = models.CharField("Estado", max_length=2, choices=States.choices)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"

    def __str__(self):
        return f"{self.name}, {self.state}"


class Address(TimeStampedModel):
    """A TimeStampedModel Address model, ordered by it's creation date"""

    zip_code = models.CharField("CEP", max_length=10)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    district = models.CharField("Bairro", max_length=255)
    street = models.CharField("Rua", max_length=255)
    number = models.CharField("Número", max_length=10)
    additional_info = models.CharField(
        "Complemento", max_length=255, null=True, blank=True
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self) -> str:
        return (
            f"{self.zip_code}:{self.street}, {self.number} - {self.additional_info} -"
            f" {self.district} - {self.city}"
        )
