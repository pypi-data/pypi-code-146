from datetime import datetime
from decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from colorfield.fields import ColorField
from payments import PurchasedItem

from aleksis.apps.tezor.models.base import Client
from aleksis.apps.tezor.models.invoice import Invoice, InvoiceGroup
from aleksis.core.mixins import ExtensibleModel
from aleksis.core.models import Group, Person
from aleksis.core.util.core_helpers import generate_random_code, get_site_preferences
from aleksis.core.util.email import send_email

from .data_checks import EventMembersSyncDataCheck


class RegistrationState(ExtensibleModel):

    name = models.CharField(verbose_name=_("Name"), max_length=255)
    colour = ColorField(blank=True, verbose_name=_("Colour"))

    def __str__(self) -> str:
        return self.name


class Terms(ExtensibleModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    term = RichTextField(verbose_name=_("Term"))
    confirmation_text = models.TextField(verbose_name=_("Confirmation text"))

    def __str__(self) -> str:
        return self.title


class InfoMailing(ExtensibleModel):
    subject = models.CharField(max_length=255, verbose_name=_("subject"))
    text = RichTextField(verbose_name=_("Text"))
    reply_to = models.EmailField(verbose_name=_("Request replies to"), blank=True)

    active = models.BooleanField(verbose_name=_("Mailing is active"), default=False)

    sender = models.EmailField(verbose_name=_("Sender"), blank=True)
    send_to_person = models.BooleanField(verbose_name=_("Send to registered person"), default=True)
    send_to_guardians = models.BooleanField(verbose_name=_("Send to guardians"), default=False)
    send_to_retracted = models.BooleanField(
        verbose_name=_("Send to participants who retracted"), default=False
    )
    send_to_not_checked_in = models.BooleanField(
        verbose_name=_("Send to participants who did not check in"), default=True
    )

    def __str__(self) -> str:
        return self.subject

    @classmethod
    def get_active_mailings(cls):
        return cls.objects.filter(active=True)

    def send(self):
        for event in self.events.all():
            through = EventInfoMailingThrough.objects.get(info_mailing=self, event=event)
            sent_to = through.sent_to.all()

            filter_args = {}
            if not self.send_to_retracted:
                filter_args["retracted"] = False
            if not self.send_to_not_checked_in:
                filter_args["checked_in"] = True

            for registration in event.registrations.filter(**filter_args):
                if registration.person in sent_to:
                    continue

                subject = self.subject.format(
                    event=event, registration=registration, person=registration.person
                )
                body = self.text.format(
                    event=event, registration=registration, person=registration.person
                )

                if self.send_to_person:
                    to = [registration.person.email]
                    if self.send_to_guardians:
                        cc = registration.person.guardians.values_list("email", flat=True).all()
                    else:
                        cc = []
                elif self.send_to_guardians:
                    to = registration.person.guardians.values_list("email", flat=True).all()
                    cc = []

                sender = self.sender or get_site_preferences()["mail__address"]
                reply_to = self.reply_to or sender

                context = {"subject": subject, "body": body}
                send_email(
                    template_name="info_mailing",
                    context=context,
                    from_email=sender,
                    recipient_list=to,
                    cc=cc,
                    headers={
                        "Reply-To": reply_to,
                    },
                )

                through.sent_to.add(registration.person)


class Event(ExtensibleModel):

    data_checks = [EventMembersSyncDataCheck]

    # Event details
    display_name = models.CharField(verbose_name=_("Display name"), max_length=255)
    linked_group = models.OneToOneField(
        Group, on_delete=models.CASCADE, verbose_name=_("Group"), related_name="linked_event"
    )
    description = models.CharField(max_length=500, verbose_name=_("Description"))
    published = models.BooleanField(default=False, verbose_name=_("Publish"))
    place = models.CharField(max_length=50, verbose_name="Place")
    slug = models.SlugField(max_length=255, verbose_name=_("Slug"), blank=True)

    # Date details
    date_event = models.DateField(verbose_name=_("Date of event"))
    date_registration = models.DateField(verbose_name=_("Registration deadline"))
    date_retraction = models.DateField(verbose_name=_("Retraction deadline"))

    # Other details
    cost = models.IntegerField(verbose_name=_("Cost in €"))
    max_participants = models.PositiveSmallIntegerField(verbose_name=_("Maximum participants"))
    information = RichTextField(verbose_name=_("Information about the event"))
    terms = models.ManyToManyField(Terms, verbose_name=_("Terms"), related_name="event", blank=True)
    info_mailings = models.ManyToManyField(
        InfoMailing,
        verbose_name=_("Info mailings"),
        related_name="events",
        through="EventInfoMailingThrough",
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.linked_group.short_name:
                self.slug = slugify(self.linked_group.short_name)
            else:
                self.slug = slugify(self.display_name)

        super().save(*args, **kwargs)
        self.sync_group_members()

    def __str__(self) -> str:
        return self.display_name

    def sync_group_members(self):
        self.linked_group.members.set(
            self.registrations.filter(retracted=False).values_list("person", flat=True)
        )

    def can_register(self, request=None):
        now = datetime.today().date()

        if request and request.user.is_authenticated:
            if request.user.person in self.linked_group.members.all():
                return False

            if EventRegistration.objects.filter(person=request.user.person).exists():
                return False

            if (
                Voucher.objects.filter(event=self, person=request.user.person, used=False).count()
                > 0
            ):
                return True

        if self.linked_group.members.count() >= self.max_participants:
            return False

        if self.date_registration:
            return self.date_registration >= now
        return self.date_event > now

    def get_absolute_url(self):
        return reverse("event_by_name", kwargs={"slug": self.slug})

    def individual_cost(self, request=None):
        if request and request.user.is_authenticated:
            if Voucher.objects.filter(event=self, person=request.user.person, used=False).exists():
                voucher = Voucher.objects.get(event=self, person=request.user.person, used=False)
                individual_cost = voucher.discount * self.cost / 100
                return individual_cost
        else:
            return self.cost

    @property
    def booked_percentage(self):
        return self.linked_group.members.count() / self.max_participants * 100

    @property
    def members_persons(self):
        return self.linked_group.members.all()

    @property
    def owners_persons(self):
        return self.linked_group.owners.all()

    @classmethod
    def upcoming_published_events(cls):
        return Event.objects.filter(published=True, date_event__gte=now())


class EventInfoMailingThrough(ExtensibleModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    info_mailing = models.ForeignKey(InfoMailing, on_delete=models.CASCADE)

    sent_to = models.ManyToManyField(
        Person,
        verbose_name=_("Sent to persons"),
        related_name="received_info_mailings",
        editable=False,
        blank=True,
    )


class Voucher(ExtensibleModel):
    class Meta:
        verbose_name = _("Vouchers")
        verbose_name_plural = _("Vouchers")

    code = models.CharField(max_length=255, blank=True, default="")
    event = models.ForeignKey(
        Event,
        related_name="vouchers",
        verbose_name=_("Event"),
        on_delete=models.CASCADE,
        null=True,
    )
    person = models.ForeignKey(
        Person,
        related_name="vouchers",
        verbose_name=_("Person"),
        on_delete=models.CASCADE,
    )
    discount = models.IntegerField(default=100)

    used = models.BooleanField(default=False)
    used_person_uid = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name=_("Used by"),
        related_name="used_vouchers",
        null=True,
    )
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_random_code(5, 3)
        super().save(*args, **kwargs)


class EventRegistration(ExtensibleModel):

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, verbose_name=_("Event"), related_name="registrations"
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name=_("Person"))
    date_registered = models.DateTimeField(auto_now_add=True, verbose_name=_("Registration date"))

    school = models.CharField(verbose_name=_("Name of school"), max_length=255)
    school_class = models.CharField(verbose_name=_("School class"), max_length=255)
    school_place = models.CharField(verbose_name=_("Place of the school"), max_length=255)

    comment = models.TextField(verbose_name=_("Comment / remarks"), blank=True, default="")
    medical_information = models.TextField(
        verbose_name=_("Medical information / intolerances"), blank=True, default=""
    )
    voucher = models.ForeignKey(
        Voucher,
        on_delete=models.CASCADE,
        verbose_name=_("Voucher"),
        blank=True,
        null=True,
    )
    donation = models.PositiveIntegerField(verbose_name=_("Donation"), blank=True, null=True)
    accepted_terms = models.ManyToManyField(
        Terms,
        verbose_name=_("Accepted terms"),
        related_name="registrations",
    )

    states = models.ManyToManyField(
        RegistrationState, verbose_name=_("States"), related_name="registrations"
    )

    retracted = models.BooleanField(verbose_name=_("Retracted"), default=False)
    retracted_date = models.DateField(verbose_name=_("Retracted at"), null=True, blank=True)

    checked_in = models.BooleanField(verbose_name=_("Checked in"), default=False)
    checked_in_date = models.DateTimeField(verbose_name=_("Checked in at"), null=True, blank=True)

    def mark_checked_in(self):
        if not self.checked_in:
            self.checked_in = True
            self.checked_in_date = now()
            self.save()
        else:
            raise ValidationError(_("Person is already checked in!"))

    def retract(self):
        # Remove person from group
        self.event.linked_group.members.remove(self.person)
        # Mark registration as retracted
        self.retracted = True
        self.retracted_date = datetime.today()
        self.save()

    def get_person(self):
        return self.person

    def get_billing_email_recipients(self):
        return [self.person.email] + list(self.person.guardians.values_list("email", flat=True))

    def get_invoice(self):
        # FIXME Maybe do not hard-code this
        client, __ = Client.objects.get_or_create(name="Teckids e.V.")
        group, __ = InvoiceGroup.objects.get_or_create(
            name="Hack'n'Fun-Veranstaltungen",
            client=client,
            defaults={
                "template_name": "paweljong/invoice_pdf.html",
            },
        )

        invoice, __ = Invoice.objects.get_or_create(
            for_content_type=ContentType.objects.get_for_model(self),
            for_object_id=self.pk,
            defaults={
                "group": group,
                "number": f"HNF-{self.date_registered.strftime('%Y-%m')}-{self.id}",
                "currency": "EUR",
                "total": self._get_total_amount()[0],
                "tax": self._get_total_amount()[1],
                "description": _("Participation of {} in event {}").format(
                    self.person.addressing_name, self.event.display_name
                ),
                "billing_first_name": self.person.first_name,
                "billing_last_name": self.person.last_name,
                "billing_address_1": f"{self.person.street} {self.person.housenumber}",
                "billing_city": self.person.place,
                "billing_postcode": self.person.postal_code,
                "billing_email": self.person.email,
            },
        )

        return invoice

    def get_purchased_items(self):
        # FIXME Maybe do not hard-code the tax rate and currency
        # First, return main amount
        yield PurchasedItem(
            name=self.event.display_name,
            quantity=1,
            price=Decimal(self.event.cost / 1.07),
            currency="EUR",
            sku="EVENT",
            tax_rate=7,
        )

        # If a dnoation was made, add it
        if self.donation:
            yield PurchasedItem(
                name=_("Social Sponsoring / Extra Donation"),
                quantity=1,
                price=Decimal(self.donation),
                currency="EUR",
                sku="DONAT",
                tax_rate=0,
            )

        # If a voucher was used, add it
        if self.voucher:
            yield PurchasedItem(
                name=_("Voucher / Granted discount"),
                quantity=1,
                price=Decimal(-1 * self.voucher.discount * (self.event.cost / 1.07) / 100),
                currency="EUR",
                sku="DISCO",
                tax_rate=7,
            )

    def _get_total_amount(self):
        total, total_tax = 0, 0
        for item in self.get_purchased_items():
            tax = item.price * item.tax_rate / 100
            total += item.price + tax
            total_tax += tax
        return total, total_tax

    def __str__(self) -> str:
        return f"{self.event}, {self.person.first_name} {self.person.last_name}"

    def save(self, *args, **kwargs):
        self.event.sync_group_members()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.event.sync_group_members()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = _("Event registration")
        verbose_name_plural = _("Event registrations")
        constraints = [
            models.UniqueConstraint(
                fields=["person", "event"], name="unique_person_registration_per_event"
            )
        ]


class Checkpoint(ExtensibleModel):
    event = models.ForeignKey(
        Event, verbose_name=_("Related event"), related_name="checkpoints", on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        Person,
        verbose_name=_("Checked person"),
        related_name="event_checkpoints",
        on_delete=models.CASCADE,
    )
    checked_by = models.ForeignKey(
        Person,
        verbose_name=_("Checked by person"),
        related_name="event_checkpoints_created",
        on_delete=models.CASCADE,
    )

    comment = models.CharField(max_length=60, verbose_name=_("Comment"))

    timestamp = models.DateTimeField(verbose_name=_("Date and time of check"), auto_now_add=True)
    lat = models.DecimalField(
        max_digits=10, decimal_places=8, verbose_name=_("Latitude of check"), blank=True, null=True
    )
    lon = models.DecimalField(
        max_digits=11, decimal_places=8, verbose_name=_("Longitude of check"), blank=True, null=True
    )
