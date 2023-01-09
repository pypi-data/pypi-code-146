from django.core.validators import MinLengthValidator
from django.db import models

from b2_utils.validators import validate_cnpj, validate_cpf

__all__ = [
    "CpfField",
    "CnpjField",
    "States",
]


class CpfField(models.CharField):
    description = "(Brazil) Cadastro de Pessoa Física"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 11
        kwargs["validators"] = [MinLengthValidator(11), validate_cpf]

        super().__init__(*args, **kwargs)


class CnpjField(models.CharField):
    description = "(Brazil) Cadastro Nacional da Pessoa Jurídica"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 14
        kwargs["validators"] = [MinLengthValidator(14), validate_cnpj]

        super().__init__(*args, **kwargs)


class States(models.TextChoices):
    AC = "AC", "Acre"
    AL = "AL", "Alagoas"
    AM = "AM", "Amazonas"
    AP = "AP", "Amapá"
    BA = "BA", "Bahia"
    CE = "CE", "Ceará"
    ES = "ES", "Espírito Santo"
    GO = "GO", "Goiás"
    MA = "MA", "Maranhão"
    MG = "MG", "Minas Gerais"
    MS = "MS", "Mato Grosso do Sul"
    MT = "MT", "Mato Grosso"
    PA = "PA", "Pará"
    PB = "PB", "Paraíba"
    PE = "PE", "Pernambuco"
    PI = "PI", "Piauí"
    PR = "PR", "Paraná"
    RJ = "RJ", "Rio de Janeiro"
    RN = "RN", "Rio Grande do Norte"
    RO = "RO", "Rondônia"
    RR = "RR", "Roraima"
    RS = "RS", "Rio Grande do Sul"
    SC = "SC", "Santa Catarina"
    SE = "SE", "Sergipe"
    SP = "SP", "São Paulo"
    TO = "TO", "Tocantins"
    DF = "DF", "Distrito Federal"
