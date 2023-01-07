from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.syndication.views import Feed
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.http import urlencode
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.generic import FormView, TemplateView, View
from django.views.generic.detail import DetailView

import reversion
from django_tables2 import RequestConfig
from django_tables2.views import SingleTableView
from formtools.wizard.views import SessionWizardView
from reversion.views import RevisionMixin
from rules.contrib.views import PermissionRequiredMixin, permission_required
from templated_email import send_templated_mail

from aleksis.apps.postbuero.models import MailAddress
from aleksis.apps.tezor.models.invoice import Invoice
from aleksis.core.mixins import AdvancedCreateView, AdvancedDeleteView, AdvancedEditView
from aleksis.core.models import Activity, Group, Person
from aleksis.core.util import messages
from aleksis.core.util.core_helpers import get_site_preferences, objectgetter_optional

from .filters import EventFilter, EventRegistrationFilter, VoucherFilter
from .forms import (
    EditEventForm,
    EditEventRegistrationForm,
    EditInfoMailingForm,
    EditTermForm,
    EditVoucherForm,
    EventCheckpointForm,
    GenerateListForm,
    PersonGroupFormPerson,
    RegistrationNotificationForm,
    RegistrationStatesForm,
)
from .models import (
    Checkpoint,
    Event,
    EventRegistration,
    InfoMailing,
    RegistrationState,
    Terms,
    Voucher,
)
from .tables import (
    AdditionalFieldsTable,
    ChildGroupsTable,
    EventRegistrationsTable,
    InfoMailingsTable,
    ManageEventsTable,
    RegistrationStatesTable,
    TermsTable,
    VouchersTable,
)

User = get_user_model()


@method_decorator(never_cache, name="dispatch")
class CreateEventView(PermissionRequiredMixin, AdvancedCreateView):
    form_class = EditEventForm
    model = Event
    permission_required = "paweljong.create_events_rule"
    template_name = "paweljong/event/create.html"
    success_url = reverse_lazy("manage_events")
    success_message = _("The event has been saved.")


@method_decorator(never_cache, name="dispatch")
class EditEventView(PermissionRequiredMixin, RevisionMixin, AdvancedEditView):
    form_class = EditEventForm
    model = Event
    slug_field = "slug"
    permission_required = "paweljong.change_event_rule"
    context_object_name = "manage_events"
    template_name = "paweljong/event/edit.html"
    success_url = reverse_lazy("manage_events")
    success_message = _("The event has been saved.")


@permission_required("paweljong.view_events_rule")
def manage_events(request: HttpRequest) -> HttpResponse:
    """List view listing all registrations."""
    context = {}

    # Get all registrations
    now = timezone.datetime.today()
    events = Event.objects.all()

    # Get filter
    events_filter = EventFilter(request.GET, queryset=events)
    context["events_filter"] = events_filter

    # Build table
    events_table = ManageEventsTable(events_filter.qs)
    RequestConfig(request).configure(events_table)
    context["events_table"] = events_table

    return render(request, "paweljong/event/manage.html", context)


@permission_required("paweljong.view_vouchers_rule")
def vouchers(request):
    context = {}

    # Get all unused vouchers
    vouchers = Voucher.objects.filter(used=False, deleted=False)

    # Get filter
    vouchers_filter = VoucherFilter(request.GET, queryset=vouchers)
    context["vouchers_filter"] = vouchers_filter

    # Build table
    vouchers_table = VouchersTable(vouchers_filter.qs)
    RequestConfig(request).configure(vouchers_table)
    context["vouchers_table"] = vouchers_table

    return render(request, "paweljong/voucher/list.html", context)


@permission_required("paweljong.generate_lists_rule")
def generate_lists(request: HttpRequest) -> HttpResponse:
    context = {}

    generate_list_form = GenerateListForm()

    if request.method == "POST":
        generate_list_form = GenerateListForm(request.POST)
        if generate_list_form.is_valid():
            context["group"] = generate_list_form.cleaned_data["group"]
            template = generate_list_form.cleaned_data["template"]
            context["landscape"] = generate_list_form.cleaned_data["landscape"]

            return render(request, "paweljong/print/%s.html" % (template), context)

    context["generate_list_form"] = generate_list_form

    return render(request, "paweljong/print/manage.html", context)


@method_decorator(never_cache, name="dispatch")
class EventRegistrationCreateView(PermissionRequiredMixin, AdvancedCreateView):
    """Create view for event registrations."""

    model = EventRegistration
    form_class = EditEventRegistrationForm
    permission_required = "paweljong.create_registration_rule"
    template_name = "paweljong/event_registration/create.html"
    success_url = reverse_lazy("registrations")
    success_message = _("The event registration has been created.")


@method_decorator(never_cache, name="dispatch")
class EventRegistrationEditView(PermissionRequiredMixin, AdvancedEditView):
    """Edit view for event registrations."""

    model = EventRegistration
    form_class = EditEventRegistrationForm
    permission_required = "paweljong.change_registration_rule"
    template_name = "paweljong/event_registration/edit.html"
    success_url = reverse_lazy("registrations")
    success_message = _("The event registration has been saved.")


@permission_required(
    "paweljong.change_registration_rule",
    fn=objectgetter_optional(EventRegistration, None, False),
)
def edit_registration(request: HttpRequest, pk) -> HttpResponse:
    context = {}

    registration = objectgetter_optional(EventRegistration, None, False)(request, pk)

    edit_event_registration_form = EditEventRegistrationForm(
        request.POST or None, instance=registration
    )

    if request.method == "POST":
        if edit_event_registration_form.is_valid():
            with reversion.create_revision():
                edit_event_registration_form.save(commit=True)

            messages.success(request, _("The registration has been saved."))

            return redirect("registration")

    context["edit_event_registration_form"] = edit_event_registration_form

    return render(request, "paweljong/event_registration/edit.html", context)


@permission_required("paweljong.view_voucher_rule", fn=objectgetter_optional(Voucher, None, False))
def print_voucher(request: HttpRequest, pk) -> HttpResponse:
    context = {}

    voucher = Voucher.objects.get(id=pk)
    context["voucher"] = voucher

    return render(request, "paweljong/print/voucher.html", context)


class EventRegistrationDetailView(PermissionRequiredMixin, DetailView):
    """Detail view for an application instance."""

    context_object_name = "registration"
    permission_required = "paweljong.view_registration_rule"
    template_name = "paweljong/event_registration/full.html"

    def get_queryset(self):
        return EventRegistration.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        invoice = self.get_object().get_invoice()
        context["invoice"] = invoice

        return context


class EventRegistrationDeleteView(PermissionRequiredMixin, AdvancedDeleteView):
    """Delete view for registrations."""

    model = EventRegistration
    permission_required = "paweljong.delete_eventregistration_rule"
    template_name = "core/pages/delete.html"
    success_url = reverse_lazy("registrations")
    success_message = _("The registration has been deleted.")


@method_decorator(never_cache, name="dispatch")
class VoucherCreateView(PermissionRequiredMixin, AdvancedCreateView):
    """Create view for vouchers."""

    model = Voucher
    form_class = EditVoucherForm
    permission_required = "paweljong.create_voucher_rule"
    template_name = "paweljong/voucher/create.html"
    success_url = reverse_lazy("vouchers")
    success_message = _("The voucher has been created.")


@method_decorator(never_cache, name="dispatch")
class VoucherEditView(PermissionRequiredMixin, AdvancedEditView):
    """Edit view for vouchers."""

    model = Voucher
    form_class = EditVoucherForm
    permission_required = "paweljong.change_voucher_rule"
    template_name = "paweljong/voucher/edit.html"
    success_url = reverse_lazy("vouchers")
    success_message = _("The voucher has been saved.")


class VoucherDeleteView(PermissionRequiredMixin, AdvancedDeleteView):
    """Delete view for vouchers."""

    model = Voucher
    permission_required = "paweljong.delete_voucher_rule"
    template_name = "core/pages/delete.html"
    success_url = reverse_lazy("vouchers")
    success_message = _("The voucher has been deleted.")


def is_person_anonymous(wizard):
    return wizard.request.user.is_anonymous


def set_email_needed(request, slug: Optional[str] = None):
    request.session["email_needed"] = True

    if slug:
        return redirect("register_event_by_slug", slug)
    else:
        return redirect("register_account")


def is_email_needed(wizard):
    return wizard.request.session.pop("email_needed", None)


TEMPLATES = {
    "email": "paweljong/event/register_wizard.html",
    "register": "paweljong/event/register_wizard.html",
    "contact_details": "paweljong/event/register_wizard.html",
    "guardians": "paweljong/event/register_wizard.html",
    "additional": "paweljong/event/register_wizard.html",
    "financial": "paweljong/event/register_wizard.html",
    "consent": "paweljong/event/register_wizard_consent.html",
}


class AccountRegisterWizardView(SessionWizardView):
    template_name = "paweljong/account_wizard.html"
    file_storage = settings.DEFAULT_FILE_STORAGE

    def get_form_kwargs(self, step):
        kwargs = super().get_form_kwargs()
        if step == "email":
            kwargs["request"] = self.request
        return kwargs

    def get_form_initial(self, step):

        initial = self.initial_dict.get(step, {})

        if step == "register":
            cleaned_data_email = self.get_cleaned_data_for_step("email")
            if cleaned_data_email:
                domain = cleaned_data_email["domain"]
                email = f"{cleaned_data_email['local_part']}@{domain.domain}"
                initial.update(
                    {
                        "email": email,
                        "email2": email,
                    }
                )

        if step == "contact_details":
            cleaned_data_register = self.get_cleaned_data_for_step("register")
            if cleaned_data_register:
                initial.update(
                    {
                        "first_name": cleaned_data_register["first_name"],
                        "last_name": cleaned_data_register["last_name"],
                        "email": cleaned_data_register["email"],
                        "date_of_birth": cleaned_data_register["date_of_birth"],
                    }
                )

        return self.initial_dict.get(step, initial)

    def done(self, form_list, **kwargs):

        cleaned_data_email = self.get_cleaned_data_for_step("email")
        cleaned_data_register = self.get_cleaned_data_for_step("register")

        # Create email address
        _email = None
        if cleaned_data_email:
            _email = MailAddress.objects.create(
                local_part=cleaned_data_email["local_part"],
                domain=cleaned_data_email["domain"],
            )

        # Create user
        if cleaned_data_register:
            user = User.objects.create(
                username=cleaned_data_register["username"],
                email=cleaned_data_register["email"],
            )
            user.set_password(cleaned_data_register["password1"])
            user.save()
        else:
            user = self.request.user

        person, created = Person.objects.get_or_create(
            user=user,
            defaults={
                "email": cleaned_data_register["email"],
                "first_name": cleaned_data_register["first_name"],
                "last_name": cleaned_data_register["last_name"],
                "date_of_birth": cleaned_data_register["date_of_birth"],
            },
        )

        if _email:
            _email.person = person
            _email.save()

        return redirect("index")


class RegisterEventWizardView(SessionWizardView):
    template_name = "paweljong/event/register_wizard.html"
    file_storage = settings.DEFAULT_FILE_STORAGE

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context["event"] = Event.objects.get(slug=self.kwargs["slug"])

        if self.steps.current == "email":
            context["info_title"] = _("Create e-mail address")
            context["info_text"] = _(
                "All participants need a personal e-mail address, which they check and read "
                "temselves. We offer the possibility to register an e-mail address "
                "on our secure servers, made for young users. For information about receiving "
                "mails, see: "
                "<a href='https://leopard.institute/pages/services.html'>https://leopard.institute/pages/services.html</a>."  # noqa
            )
        elif self.steps.current == "register":
            context["info_title"] = _("Event registration")
            context["info_text"] = _(
                "First, please enter some basic information about yourself, and check "
                "whether all information is correct."
            )
        elif self.steps.current == "contact_details":
            context["info_title"] = _("Contact information")
            context["info_text"] = _(
                "Tell us how we can contact you. You will receive information about "
                "the event by e-mail. Please use your personal e-mail address "
                "where you will read mails yourself, not an address of your parents. "
                "We will always send all important information to your parents as well, "
                "and you will enter their e-mail address on the next page."
            )
        elif self.steps.current == "guardians":
            context["info_title"] = _("Legal guardians / parents")
            context["info_text"] = _(
                "Tell us how we can reach your parents or other legal guardians. "
                "This should be the person who was present when you registered for the "
                "event (which is now). If you want to add another parent, please tell us "
                "later as a comment."
            )
        elif self.steps.current == "additional":
            context["info_title"] = _("Additional registration information")
            context["info_text"] = _(
                "Please answer the following questions as precisely as you can, so "
                "we can make sure your event attendance will be organised as wel las possible."
            )
        elif self.steps.current == "financial":
            context["info_title"] = _("Payment")
            context["info_text"] = _(
                "Please decide with your parents how you want to pay. In this step, "
                "you only select a payment method. The real payment will be done "
                "in a separate step, after the registration is complete."
            )
        elif self.steps.current == "consent":
            context["info_title"] = _("Consent")
            context["info_text"] = _(
                "Lastly, please read the terms and conditions carefully, together "
                "with your parents. After that, you will need to confirm that you "
                "agree with everything yourself, and that your parents also agree."
            )

        return context

    def get_form_kwargs(self, step):
        kwargs = super().get_form_kwargs()
        if step == "email":
            kwargs["request"] = self.request
        if step == "additional":
            event = Event.objects.get(slug=self.kwargs["slug"])
            kwargs["event"] = event
        if step == "consent":
            event = Event.objects.get(slug=self.kwargs["slug"])
            kwargs["event"] = event
        return kwargs

    def get_form_initial(self, step):

        initial = self.initial_dict.get(step, {})

        if step == "register":
            cleaned_data_email = self.get_cleaned_data_for_step("email")
            if cleaned_data_email:
                domain = cleaned_data_email["domain"]
                email = f"{cleaned_data_email['local_part']}@{domain.domain}"
                initial.update(
                    {
                        "email": email,
                        "email2": email,
                    }
                )

        if step == "guardians":
            if hasattr(self.request.user, "person"):
                person = self.request.user.person
                if person.guardians.first():
                    initial.update(
                        {
                            "guardian_first_name": person.guardians.first().first_name,
                            "guardian_last_name": person.guardians.first().last_name,
                            "guardian_mobile_number": person.guardians.first().mobile_number,
                            "guardian_email": person.guardians.first().email,
                        }
                    )

        if step == "contact_details":
            if hasattr(self.request.user, "person"):
                person = self.request.user.person
                initial.update(
                    {
                        "first_name": person.first_name,
                        "last_name": person.last_name,
                        "mobile_number": person.mobile_number,
                        "email": person.email,
                        "street": person.street,
                        "place": person.place,
                        "housenumber": person.housenumber,
                        "sex": person.sex,
                        "date_of_birth": person.date_of_birth,
                        "postal_code": person.postal_code,
                    }
                )

            else:
                cleaned_data_register = self.get_cleaned_data_for_step("register")
                if cleaned_data_register:
                    initial.update(
                        {
                            "first_name": cleaned_data_register["first_name"],
                            "last_name": cleaned_data_register["last_name"],
                            "email": cleaned_data_register["email"],
                            "date_of_birth": cleaned_data_register["date_of_birth"],
                        }
                    )

        return self.initial_dict.get(step, initial)

    def done(self, form_list, **kwargs):

        event = Event.objects.get(slug=self.kwargs["slug"])
        cleaned_data_email = self.get_cleaned_data_for_step("email")
        cleaned_data_contact_details = self.get_cleaned_data_for_step("contact_details")
        cleaned_data_guardians = self.get_cleaned_data_for_step("guardians")
        cleaned_data_register = self.get_cleaned_data_for_step("register")
        cleaned_data_additional = self.get_cleaned_data_for_step("additional")
        cleaned_data_financial = self.get_cleaned_data_for_step("financial")
        cleaned_data_consent = self.get_cleaned_data_for_step("consent")

        if cleaned_data_financial["voucher_code"]:
            vouchers = Voucher.objects.filter(
                person=person, event=event, used=False, code=cleaned_data_financial["voucher_code"]
            )
            if vouchers:
                voucher = vouchers.first()
            else:
                messages.error(self.request, _("You entered an invalid voucher code!"))

        # Create email address
        if cleaned_data_email:
            _email = MailAddress.objects.create(
                local_part=cleaned_data_email["local_part"],
                domain=cleaned_data_email["domain"],
            )

        # Create user
        if cleaned_data_register:
            user = User.objects.create(
                username=cleaned_data_register["username"],
                email=cleaned_data_register["email"],
            )
            user.set_password(cleaned_data_register["password1"])
            user.save()
        else:
            user = self.request.user

        person, created = Person.objects.get_or_create(
            user=user,
            defaults={
                "email": cleaned_data_contact_details["email"],
                "first_name": cleaned_data_contact_details["first_name"],
                "last_name": cleaned_data_contact_details["last_name"],
            },
        )

        if (
            "mobile_number" in cleaned_data_contact_details
            or "sex" in cleaned_data_contact_details
            or "date_of_birth" in cleaned_data_contact_details
        ):
            person.mobile_number = cleaned_data_contact_details["mobile_number"]
            person.sex = cleaned_data_contact_details["sex"]
            person.date_of_birth = cleaned_data_contact_details["date_of_birth"]

            person.save()

        # Store postal address in database
        if (
            "postal_code" in cleaned_data_contact_details
            or "place" in cleaned_data_contact_details
            or "street" in cleaned_data_contact_details
        ):

            person.street = cleaned_data_contact_details["street"]
            person.postal_code = cleaned_data_contact_details["postal_code"]
            person.place = cleaned_data_contact_details["place"]
            person.housenumber = cleaned_data_contact_details["housenumber"]
            person.save()

        if (
            "guardian_first_name" in cleaned_data_guardians
            or "guardian_last_name" in cleaned_data_guardians
            or "guardian_mobile_number" in cleaned_data_guardians
            or "guardian_email" in cleaned_data_guardians
        ):
            guardian, created = Person.objects.get_or_create(
                defaults={
                    "mobile_number": cleaned_data_guardians["guardian_mobile_number"],
                },
                first_name=cleaned_data_guardians["guardian_first_name"],
                last_name=cleaned_data_guardians["guardian_last_name"],
                email=cleaned_data_guardians["guardian_email"],
            )

            person.guardians.add(guardian)
            person.save()

        if cleaned_data_email:
            _email.person = person
            _email.save()

        registration = EventRegistration.objects.create(
            event=event,
            person=person,
            medical_information=cleaned_data_additional["medical_information"],
            donation=cleaned_data_financial["donation"],
            school=cleaned_data_contact_details["school"],
            school_class=cleaned_data_contact_details["school_class"],
            school_place=cleaned_data_contact_details["school_place"],
        )
        for field in event.linked_group.additional_fields.all():
            registration.extended_data[
                slugify(field.title).replace("-", "_")
            ] = cleaned_data_additional[field.title]

        for field in cleaned_data_consent:
            if not field.startswith("consent_"):
                continue
            pk = int(field.split("_")[1])
            term = Terms.objects.get(id=pk)
            registration.accepted_terms.add(term)

        registration.save()

        if cleaned_data_financial["voucher_code"]:
            vouchers = Voucher.objects.filter(
                person=person, event=event, used=False, code=cleaned_data_financial["voucher_code"]
            )
            if vouchers:
                voucher = vouchers.first()
                registration.voucher = voucher
                voucher.used = True
                with reversion.create_revision():
                    voucher.save()
                    registration.save()
            else:
                messages.error(self.request, _("You entered an invalid voucher code!"))

        invoice = registration.get_invoice()
        invoice.variant = cleaned_data_financial["payment_method"]
        invoice.save()

        context = {}
        context["registration"] = registration

        send_templated_mail(
            template_name="event_registered",
            from_email=get_site_preferences()["mail__address"],
            recipient_list=[get_site_preferences()["paweljong__event_notification_recipient"]],
            headers={
                "reply_to": [
                    person.email,
                    person.guardians.first().email,
                ],
                "X-Zammad-Customer-Email": person.email,
            },
            context=context,
        )

        messages.success(
            self.request,
            _(
                "You have successfully registered for the event. Please give us "
                "up to two days to process your registration. You will then "
                "receive an email from us."
            ),
        )

        act = Activity(
            title=_("You registered for an event"),
            description=_("You registered for the event %s" % event.display_name),
            app="Paweljong",
            user=person,
        )

        return redirect("do_payment", invoice.token)


class EventFullView(PermissionRequiredMixin, DetailView):

    model = Event
    slug_field = "slug"
    template_name = "paweljong/event/full.html"
    object_context_name = "event"
    permission_required = "paweljong.view_event_rule"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["can_register"] = context["event"].can_register(request=self.request)
        context["is_authenticated"] = self.request.user.is_authenticated
        context["individual_cost"] = context["event"].individual_cost(request=self.request)

        return context


class RegisterEventStart(PermissionRequiredMixin, DetailView):

    model = Event
    slug_field = "slug"
    template_name = "paweljong/event/register_start.html"
    object_context_name = "event"
    permission_required = "paweljong.view_event_rule"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["can_register"] = context["event"].can_register(request=self.request)
        return context


class TermListView(PermissionRequiredMixin, SingleTableView):
    """Table of all terms."""

    model = Terms
    table_class = TermsTable
    permission_required = "paweljong.view_terms_rule"
    template_name = "paweljong/term/list.html"


@method_decorator(never_cache, name="dispatch")
class TermCreateView(PermissionRequiredMixin, AdvancedCreateView):
    """Create view for terms."""

    model = Terms
    form_class = EditTermForm
    permission_required = "paweljong.create_terms_rule"
    template_name = "paweljong/term/create.html"
    success_url = reverse_lazy("terms")
    success_message = _("The term has been created.")


@method_decorator(never_cache, name="dispatch")
class TermEditView(PermissionRequiredMixin, AdvancedEditView):
    """Edit view for terms."""

    model = Terms
    form_class = EditTermForm
    permission_required = "paweljong.change_terms_rule"
    template_name = "paweljong/term/edit.html"
    success_url = reverse_lazy("terms")
    success_message = _("The term has been saved.")


class UpcomingEventsRSSFeed(Feed):
    """RSS feed for published, upcoming events."""

    def title(self):
        return _("Upcoming events")

    def link(self):
        return reverse("index")

    def feed_url(self):
        return reverse("upcoming_events_rss_feed")

    def description(self):
        return _("Announcement feed of all upcoming events")

    def ttl(self):
        date_event = Event.upcoming_published_events().order_by("-date_event").first().date_event
        date_now = timezone.now().date()

        return (date_event - date_now).seconds

    def items(self):
        return Event.upcoming_published_events()

    def item_title(self, item):
        return item.display_name

    def item_description(self, item):
        return item.description


class AccountRegisterStart(TemplateView):

    template_name = "paweljong/register_start.html"


class InfoMailingListView(PermissionRequiredMixin, SingleTableView):
    """Table of all info mailings."""

    model = InfoMailing
    table_class = InfoMailingsTable
    permission_required = "paweljong.view_info_mailings_rule"
    template_name = "paweljong/info_mailing/list.html"


@method_decorator(never_cache, name="dispatch")
class InfoMailingCreateView(PermissionRequiredMixin, AdvancedCreateView):
    """Create view for info mailings."""

    model = InfoMailing
    form_class = EditInfoMailingForm
    permission_required = "paweljong.create_info_mailing_rule"
    template_name = "paweljong/info_mailing/create.html"
    success_url = reverse_lazy("info_mailings")
    success_message = _("The info mailing has been created.")


@method_decorator(never_cache, name="dispatch")
class InfoMailingEditView(PermissionRequiredMixin, AdvancedEditView):
    """Edit view for info mailings."""

    model = InfoMailing
    form_class = EditInfoMailingForm
    permission_required = "paweljong.change_info_mailing_rule"
    template_name = "paweljong/info_mailing/edit.html"
    success_url = reverse_lazy("info_mailings")
    success_message = _("The info mailing has been saved.")


class InfoMailingDeleteView(PermissionRequiredMixin, AdvancedDeleteView):
    """Delete view for info mailings."""

    model = InfoMailing
    permission_required = "paweljong.delete_info_mailing_rule"
    template_name = "core/pages/delete.html"
    success_url = reverse_lazy("info_mailings")
    success_message = _("The info mailing has been deleted.")


class SendMailFromRegistration(PermissionRequiredMixin, FormView):

    template_name = "paweljong/event_registration/notification.html"
    permission_required = "paweljong.send_notification_mail_rule"
    form_class = RegistrationNotificationForm
    success_url = reverse_lazy("registrations")

    def form_valid(self, form):

        registration = EventRegistration.objects.get(id=self.kwargs["pk"])

        context = {}
        recipient_list = []
        context["subject"] = form.cleaned_data["subject"]
        context["registration"] = registration
        context["body"] = form.cleaned_data["text"]

        if form.cleaned_data["reply_to"]:
            reply_to = form.cleaned_data["reply_to"]
        else:
            reply_to = form.cleaned_data["sender"]
        if form.cleaned_data["send_to_person"]:
            recipient_list.append(registration.person.email)
        if form.cleaned_data["send_to_guardians"]:
            recipient_list.append(registration.person.guardians.first().email)

        send_templated_mail(
            template_name="event_notification",
            from_email=get_site_preferences()["mail__address"],
            recipient_list=recipient_list,
            headers={
                "reply_to": reply_to,
            },
            context=context,
        )

        return super().form_valid(self)


class RegistrationStateListView(PermissionRequiredMixin, SingleTableView):
    """Table of all terms."""

    model = RegistrationState
    table_class = RegistrationStatesTable
    permission_required = "paweljong.view_registration_states_rule"
    template_name = "paweljong/registration_state/list.html"


@method_decorator(never_cache, name="dispatch")
class RegistrationStateCreateView(PermissionRequiredMixin, AdvancedCreateView):
    """Create view for terms."""

    model = RegistrationState
    form_class = RegistrationStatesForm
    permission_required = "paweljong.create_registration_states_rule"
    template_name = "paweljong/registration_state/create.html"
    success_url = reverse_lazy("registration_states")
    success_message = _("The term has been created.")


@method_decorator(never_cache, name="dispatch")
class RegistrationStateEditView(PermissionRequiredMixin, AdvancedEditView):
    """Edit view for terms."""

    model = RegistrationState
    form_class = RegistrationStatesForm
    permission_required = "paweljong.change_registration_states_rule"
    template_name = "paweljong/registration_state/edit.html"
    success_url = reverse_lazy("registration_states")
    success_message = _("The term has been saved.")


class RetractRegistration(PermissionRequiredMixin, View):

    permission_required = "paweljong.can_retract_registration_rule"

    def get_object(self, *args, **kwargs):
        return EventRegistration.objects.get(id=self.kwargs["pk"])

    def get(self, *args, **kwargs):
        registration = self.get_object()

        registration.retract()
        messages.success(self.request, _("Registration successfully retracted."))

        return redirect("event_detail_by_name", slug=registration.event.slug)


class EventDetailView(PermissionRequiredMixin, DetailView):
    """Detail view for an event instance."""

    context_object_name = "event"
    permission_required = "paweljong.view_event_detail_rule"
    template_name = "paweljong/event/detail.html"
    model = Event
    slug_field = "slug"

    def get_queryset(self):
        return Event.objects.all()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        registrations = EventRegistration.objects.filter(event=self.object)
        registrations_filter = EventRegistrationFilter(self.request.GET, queryset=registrations)
        context["registrations_filter"] = registrations_filter

        # Registrations table
        registrations_table = EventRegistrationsTable(registrations_filter.qs)
        RequestConfig(self.request).configure(registrations_table)
        context["registrations_table"] = registrations_table

        # Child groups table
        child_groups = self.object.linked_group.child_groups.all()
        child_groups_table = ChildGroupsTable(child_groups)
        RequestConfig(self.request).configure(child_groups_table)
        context["child_groups_table"] = child_groups_table

        # Additional fields table
        additional_fields = self.object.linked_group.additional_fields.all()
        additional_fields_table = AdditionalFieldsTable(additional_fields)
        RequestConfig(self.request).configure(additional_fields_table)
        context["additional_fields_table"] = additional_fields_table

        return context


class PersonGroupView(PermissionRequiredMixin, FormView):

    template_name = "paweljong/event/persons_group.html"
    permission_required = "paweljong.add_persons_to_group_rule"
    form_class = PersonGroupFormPerson

    def form_valid(self, form):

        group = Group.objects.get(id=self.kwargs["pk"])

        try:
            person = Person.objects.get(user__username=form.cleaned_data["username"])
            group.members.add(person)
            messages.success(self.request, _(f"Person {person} added successfully!"))
        except Person.DoesNotExist:
            messages.error(self.request, _("Person does not exist!"))

        return super().form_valid(self)

    def get_success_url(self):
        return reverse("add_persons_to_group", kwargs={"pk": self.kwargs["pk"]})


class EventCheckpointView(PermissionRequiredMixin, FormView):

    template_name = "paweljong/event/checkpoint.html"
    permission_required = "paweljong.event_checkpoint_rule"
    form_class = EventCheckpointForm

    def get_object(self):
        return Event.objects.get(slug=self.kwargs["slug"])

    def get_initial(self):
        initial = super().get_initial() or {}
        if "comment" in self.request.GET:
            initial["comment"] = self.request.GET.get("comment")
        return initial

    def form_valid(self, form):
        checkpoint = Checkpoint()

        checkpoint.event = get_object_or_404(Event, slug=self.kwargs["slug"])
        try:
            checkpoint.person = Person.objects.get(user__username=form.cleaned_data["username"])
        except Person.DoesNotExist:
            messages.error(self.request, _("The provided username is not linked to a person."))
        checkpoint.checked_by = self.request.user.person

        checkpoint.comment = form.cleaned_data["comment"]
        checkpoint.timestamp = timezone.now()
        if form.cleaned_data["use_latlon"]:
            checkpoint.lat = form.cleaned_data["lat"]
            checkpoint.lon = form.cleaned_data["lon"]

        checkpoint.save()
        messages.success(
            self.request,
            _("{} successfully checked for {}.").format(
                str(checkpoint.person), str(checkpoint.comment)
            ),
        )
        self._comment = checkpoint.comment
        return super().form_valid(self)

    def get_success_url(self):
        return (
            reverse("event_by_name_checkpoint", kwargs={"slug": self.kwargs["slug"]})
            + "?"
            + urlencode({"comment": self._comment})
        )


class ViewTerms(PermissionRequiredMixin, DetailView):

    context_object_name = "event"
    template_name = "paweljong/event/terms.html"
    permission_required = "paweljong.can_view_terms_rule"
    model = Event
    slug_field = "slug"


class CheckInRegistration(PermissionRequiredMixin, View):

    permission_required = "paweljong.change_registration_rule"

    def get_object(self, *args, **kwargs):
        return EventRegistration.objects.get(id=self.kwargs["pk"])

    def get(self, *args, **kwargs):
        registration = self.get_object()

        try:
            registration.mark_checked_in()
            messages.success(self.request, _("Successfully checked in."))
        except ValidationError:
            messages.error(self.request, _("Person is already checked in!"))

        return redirect("event_detail_by_name", slug=registration.event.slug)


class MarkRegistrationPayed(PermissionRequiredMixin, View):

    permission_required = "paweljong.mark_payment_payed_rule"

    def get_object(self, *args, **kwargs):
        registration = EventRegistration.objects.get(id=self.kwargs["pk"])
        invoice = registration.get_invoice()
        return invoice

    def get(self, *args, **kwargs):
        invoice = self.get_object()

        invoice.status = "confirmed"
        invoice.save()
        messages.success(request, _("Successfully marked as payed!"))

        return redirect("registration_by_pk", pk=invoice.for_object.pk)
