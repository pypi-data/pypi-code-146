from django.db.models.signals import post_save
from django.dispatch import receiver

from aleksis.core.models import Person
from aleksis.core.util.core_helpers import get_site_preferences

from .models.invoice import Invoice


@receiver(post_save, sender=Person)
def update_on_person_change(sender, instance, **kwargs):

    if get_site_preferences()["payments__update_on_person_change"]:
        Invoice.objects.filter(person=instance, status__in=("waiting", "input", "preauth")).update(
            billing_email=instance.email,
            billing_first_name=instance.first_name,
            billing_last_name=instance.last_name,
            billing_address_1=f"{instance.street} {instance.housenumber}",
            billing_postcode=instance.postal_code,
            billing_city=instance.place,
        )
