from django import forms
from django.forms import fields
from django.utils import dateformat, formats
from django.utils.translation import gettext_lazy as _

from allauth.account.views import SignupForm
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
from material import Fieldset, Layout, Row
from phonenumber_field.formfields import PhoneNumberField

from aleksis.apps.tezor.models.invoice import InvoiceGroup
from aleksis.core.mixins import ExtensibleForm
from aleksis.core.models import Group, Person

from .models import Event, EventRegistration, InfoMailing, RegistrationState, Terms, Voucher

COMMENT_CHOICES = [
    ("first", _("Only first name")),
    ("first_age", _("First name and age")),
    ("first_last_age", _("First name, last name and age")),
]

TEMPLATE_CHOICES = [
    ("list_sign", _("Signature list")),
    ("list_participants", _("Participants list")),
    ("corona", _("Corona attendance list")),
]

LICENCE_CHOICES = [
    ("CC-BY-4.0+", _("Creative Commons with attribution, 4.0 or later")),
    (
        "CC-BY-SA-4.0+",
        _(
            "Creative Commons with attribution and distribution only "
            "under the same conditions, 4.0 or later"
        ),
    ),
]


class EditEventForm(ExtensibleForm):
    """Form to create or edit an event."""

    layout = Layout(
        Fieldset(
            _("Base data"),
            "linked_group",
            Row("display_name", "slug", "description"),
            Row("place", "published"),
            Fieldset(_("Date data"), Row("date_event", "date_registration", "date_retraction")),
            Fieldset(_("Event details"), Row("cost", "max_participants"), "information"),
            Fieldset(_("Terms"), "terms"),
            Fieldset(_("Info mailings"), "info_mailings"),
        ),
    )

    class Meta:
        model = Event
        fields = [
            "linked_group",
            "display_name",
            "description",
            "slug",
            "place",
            "published",
            "date_event",
            "date_registration",
            "date_retraction",
            "cost",
            "max_participants",
            "terms",
            "information",
            "info_mailings",
        ]
        widgets = {
            "linked_group": ModelSelect2Widget(
                search_fields=["name__icontains"],
                attrs={"data-minimum-input-length": 0, "class": "browser-default"},
            ),
            "terms": ModelSelect2MultipleWidget(
                search_fields=["aspect__icontains"],
                attrs={"data-minimum-input-length": 0, "class": "browser-default"},
            ),
            "info_mailings": ModelSelect2MultipleWidget(
                search_fields=["subject__icontains"],
                attrs={"data-minimum-input-length": 0, "class": "browser-default"},
            ),
        }


class EditVoucherForm(forms.ModelForm):
    """Form to edit and create vouchers."""

    class Meta:
        model = Voucher
        exclude = ["code", "used_person_uid", "used", "deleted"]
        widgets = {
            "event": ModelSelect2Widget(
                search_fields=["display_name__icontains"],
                attrs={"data-minimum-input-length": 0, "class": "browser-default"},
            ),
            "person": ModelSelect2Widget(
                search_fields=["first_name__icontains", "last_name__icontains"],
                attrs={"data-minimum-input-length": 0, "class": "browser-default"},
            ),
        }
        help_texts = {
            "event": _("Event the voucher is valid for"),
            "person": _("Person the voucher is valid for"),
            "discount": _("Voucher discount"),
        }


class GenerateListForm(forms.Form):
    """Form to create a list of participants of a group."""

    group = forms.ModelChoiceField(
        label=_("Group"),
        queryset=Group.objects.all(),
        help_text=_("Select group to generate list"),
    )

    template = forms.ChoiceField(
        label=_("Template"),
        choices=TEMPLATE_CHOICES,
        help_text=_("Select template to generate list"),
    )

    landscape = forms.BooleanField(
        label=_("Landscape"),
        help_text=_("Select if output should be in landscape"),
        required=False,
    )


class RegisterEventGuardians(ExtensibleForm):
    class Meta:
        model = EventRegistration
        fields = []

    layout = Layout(
        Fieldset(
            _("Guardians personal data"),
            Row("guardian_first_name", "guardian_last_name"),
        ),
        Fieldset(
            _("Guardians contact details"),
            Row("guardian_email", "guardian_mobile_number"),
        ),
    )

    guardian_first_name = forms.CharField(
        label=_("Guardian's first name"),
        help_text=_(
            "Please enter the first name of the legal guardian who will fill in the registration "
            "with you and who can be reached during the event in an emergency."
        ),
    )

    guardian_last_name = forms.CharField(
        label=_("Guardian's last name"),
        help_text=_(
            "Please enter the last name of the legal guardian who will fill in the registration "
            "with you and who can be reached during the event in an emergency."
        ),
    )

    guardian_mobile_number = PhoneNumberField(
        label=_("Guardian's mobile number"),
        help_text=_(
            "We need the mobile phone number for emergencies if we "
            "urgently need to reach your parents during the event."
        ),
    )

    guardian_email = forms.EmailField(
        label=_("Guardian's email address"),
    )


class RegisterEventContactDetails(ExtensibleForm):
    class Meta:
        model = Group
        fields = []

    layout = Layout(
        Fieldset(
            _("Personal data"),
            Row("first_name", "last_name"),
            Row("date_of_birth", "sex"),
        ),
        Fieldset(
            _("Address data"),
            Row("street", "housenumber"),
            Row("postal_code", "place"),
        ),
        Fieldset(
            _("Contact details"),
            Row("mobile_number", "email"),
        ),
        Fieldset(
            _("School details"),
            Row("school", "school_place", "school_class"),
        ),
    )

    first_name = forms.CharField(
        label=_("First name"),
        disabled=True,
    )

    last_name = forms.CharField(
        label=_("Last name"),
        disabled=True,
    )

    street = forms.CharField(
        label=_("Street"),
    )

    housenumber = forms.CharField(
        label=_("Housenumber"),
    )

    postal_code = forms.CharField(
        label=_("Postal code"),
    )

    place = forms.CharField(
        label=_("Place"),
    )

    mobile_number = PhoneNumberField(
        label=_("Mobile number"),
        required=False,
        help_text=_(
            "Your mobile number helps us to reach you in an emergency during the event, e.g. "
            "if you are alone with your group at a conference or similar. If you don't have a "
            "cell phone, you can leave the field blank."
        ),
    )

    date_of_birth = forms.DateField(
        label=_("Date of birth"),
    )

    sex = forms.ChoiceField(
        label=_("Sex"),
        help_text=_(
            "For various reasons, e.g. because we have to keep gender segregation during the night "
            "for legal reasons, we need to know if you are a boy or a girl."
        ),
        choices=Person.SEX_CHOICES,
        initial=None,
    )

    email = forms.EmailField(
        label=_("Email address"),
        help_text=_(
            "Please use your personal e-mail address here, which you will check "
            "personally. Important information will always be sent to your parents "
            "as well. Do not use an e-mail address owned by your parents here."
        ),
    )

    school = forms.CharField(
        label=_("School"),
        help_text=_("Please enter the name of your school."),
    )

    school_place = forms.CharField(
        label=_("School place"),
        help_text=_("Enter the place (city) where your school is located."),
    )

    school_class = forms.CharField(
        label=_("School class"),
        help_text=_("Please enter the class you are in (e.g. 8a)."),
    )


class RegisterEventAdditional(ExtensibleForm):

    layout = Layout(
        Fieldset(
            _("Medical information / intolerances"),
            Row("medical_information"),
        ),
        Fieldset(
            _("Other remarks"),
            Row("comment"),
        ),
    )

    class Meta:
        model = EventRegistration
        fields = ["medical_information", "comment"]
        help_texts = {
            "medical_information": _(
                "If there are any medically important things we need to "
                "consider, e.g. when making food or to make sure you take "
                "prescribed medication, please enter it here."
            ),
            "comment": _("You can write down any remarks you want to tell us here."),
        }

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__class__.layout_filled = getattr(self.__class__, "layout_filled", False)

        for field in event.linked_group.additional_fields.all():
            field_instance = getattr(fields, field.field_type)(
                required=field.required,
                help_text=field.help_text,
            )
            self.fields[field.title] = field_instance
            if not self.layout_filled:
                node = Fieldset(f"{field.title}", f"{field.title}")
                self.add_node_to_layout(node)
        self.__class__.layout_filled = True


class RegisterEventFinancial(ExtensibleForm):
    """Form to register for an event."""

    layout = Layout(
        Fieldset(
            _("Financial data"),
            "payment_method",
            Row("voucher_code", "donation"),
        ),
    )

    voucher_code = forms.CharField(
        label=_("Voucher code"),
        help_text=_("If you have a voucher code, type it in here."),
        required=False,
    )

    payment_method = forms.ChoiceField(
        label=_("Payment method"),
        help_text=_(
            "Please choose a payment method. "
            "The actual payment will be made after the registration."
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["payment_method"].choices = InvoiceGroup.objects.get(
            name="Hack'n'Fun-Veranstaltungen"
        ).get_variant_choices()

    class Meta:
        model = EventRegistration
        fields = ["voucher_code", "donation"]
        help_texts = {
            "donation": _(
                "Our association would like to offer all children and young "
                "people the opportunity to participate in our events. Sometimes, "
                "however, families cannot afford the full fee. We therefore have a "
                "budget from which we can promote participation after we have "
                "carefully examined the necessity and eligibility. We rely on "
                "donations for this budget. If you would like to donate a voluntary "
                "additional amount for this budget, please indicate this here."
            ),
        }


class RegisterEventConsent(ExtensibleForm):
    class Meta:
        model = EventRegistration
        fields = []

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in event.terms.all():
            field_instance = forms.BooleanField(
                required=True,
                label=field.confirmation_text,
            )
            self.fields[f"consent_{field.pk}"] = field_instance
            node = Row(f"consent_{field.pk}")
            self.add_node_to_layout(node)

        if event.date_retraction:
            field_instance = forms.BooleanField(
                required=True,
                label=_(
                    "I confirm that the retraction of the registration is not possible anymore "
                    "after {}"
                ).format(
                    dateformat.format(event.date_retraction, formats.get_format("DATE_FORMAT"))
                ),
            )
            self.fields["retraction_deadline"] = field_instance
            node = Row("retraction_deadline")
            self.add_node_to_layout(node)


class EditEventRegistrationForm(forms.ModelForm):

    layout = Layout(
        Row("event", "person"),
        Row("comment", "medical_information"),
        "voucher",
        Row("donation"),
        "accepted_terms",
        Row("school", "school_class", "school_place"),
        "states",
    )

    class Meta:
        model = EventRegistration
        exclude = []


class EditTermForm(forms.ModelForm):
    class Meta:
        model = Terms
        exclude = []


class RegisterEventAccount(SignupForm, ExtensibleForm):
    """Form to register new user accounts."""

    class Meta:
        model = EventRegistration
        fields = []

    layout = Layout(
        Fieldset(
            _("Base data"),
            Row("first_name", "last_name", "date_of_birth"),
        ),
        Fieldset(
            _("Account data"),
            "username",
            Row("email", "email2"),
            Row("password1", "password2"),
        ),
    )

    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))
    date_of_birth = forms.DateField(label=_("Date of birth"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].help_text = _(
            "The username must only contain lower case letters and numbers, "
            "and must begin with a letter."
        )


class EditInfoMailingForm(forms.ModelForm):

    layout = Layout(
        Row("sender", "reply_to", "active"),
        Row("send_to_person", "send_to_guardians", "send_to_retracted", "send_to_not_checked_in"),
        Row("subject"),
        Row("text"),
    )

    class Meta:
        model = InfoMailing
        exclude = ["sent_to"]


class RegistrationNotificationForm(forms.ModelForm):

    layout = Layout(
        Row("sender", "reply_to"),
        Row("send_to_person", "send_to_guardians"),
        Row("subject"),
        Row("text"),
    )

    class Meta:
        model = InfoMailing
        exclude = ["sent_to", "active"]


class RegistrationStatesForm(forms.ModelForm):
    class Meta:
        model = RegistrationState
        exclude = []


class PersonGroupFormPerson(forms.Form):
    class Media:
        js = ("https://unpkg.com/html5-qrcode", "js/paweljong/qrscanner.js")

    layout = Layout("username")

    username = forms.CharField(
        required=True,
        label=_("Person"),
        widget=forms.TextInput(attrs={"autofocus": "", "autocomplete": "off"}),
        help_text=_("Please enter a username."),
    )


class EventCheckpointForm(forms.Form):
    class Media:
        js = (
            "https://unpkg.com/html5-qrcode",
            "js/paweljong/qrscanner.js",
            "js/paweljong/checkpoint.js",
        )

    layout = Layout("comment", "use_latlon", "username")

    comment = forms.CharField(
        required=True,
        label=_("Comment"),
        help_text=_("Please enter a comment describing the checkpoint (e.g. Dinner)."),
    )

    username = forms.CharField(
        required=True,
        label=_("Person"),
        help_text=_("Please enter a username."),
        widget=forms.TextInput(attrs={"autofocus": "", "autocomplete": "off"}),
    )

    use_latlon = forms.BooleanField(
        required=False,
        label=_("Submit geolocation"),
        initial=True,
    )

    lat = forms.DecimalField(
        required=False,
        min_value=-90.0,
        max_value=90.0,
        max_digits=10,
        decimal_places=8,
        widget=forms.HiddenInput(),
    )
    lon = forms.DecimalField(
        required=False,
        min_value=-180.0,
        max_value=180.0,
        max_digits=11,
        decimal_places=8,
        widget=forms.HiddenInput(),
    )
