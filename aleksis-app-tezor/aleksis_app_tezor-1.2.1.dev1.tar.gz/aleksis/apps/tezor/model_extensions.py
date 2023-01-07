from django.utils.translation import gettext as _

from jsonstore import CharField

from aleksis.core.models import Person

Person.field(
    external_accounting_number=CharField(verbose_name=_("External accounting number"), blank=True)
)
