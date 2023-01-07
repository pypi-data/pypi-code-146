from django.urls import path

from aleksis.apps.postbuero.forms import MailAddForm

from . import views
from .forms import (
    RegisterEventAccount,
    RegisterEventAdditional,
    RegisterEventConsent,
    RegisterEventContactDetails,
    RegisterEventFinancial,
    RegisterEventGuardians,
)

register_forms = [
    ("email", MailAddForm),
    ("register", RegisterEventAccount),
    ("contact_details", RegisterEventContactDetails),
    ("guardians", RegisterEventGuardians),
    ("additional", RegisterEventAdditional),
    ("financial", RegisterEventFinancial),
    ("consent", RegisterEventConsent),
]
condition_dict = {
    "email": views.is_email_needed,
    "register": views.is_person_anonymous,
}

account_forms = [
    ("email", MailAddForm),
    ("register", RegisterEventAccount),
]

account_conditions = {
    "email": views.is_email_needed,
}

urlpatterns = [
    path("event/<slug:slug>/edit", views.EditEventView.as_view(), name="edit_event_by_slug"),
    path("event/<slug:slug>/terms", views.ViewTerms.as_view(), name="view_event_terms_by_slug"),
    path(
        "event/<slug:slug>/register",
        views.RegisterEventWizardView.as_view(register_forms, condition_dict=condition_dict),
        name="register_event_by_slug",
    ),
    path(
        "group_persons/<int:pk>/add",
        views.PersonGroupView.as_view(),
        name="add_persons_to_group",
    ),
    path("event/<slug:slug>", views.EventFullView.as_view(), name="event_by_name"),
    path("event/<slug:slug>/detail", views.EventDetailView.as_view(), name="event_detail_by_name"),
    path(
        "event/<slug:slug>/checkpoint",
        views.EventCheckpointView.as_view(),
        name="event_by_name_checkpoint",
    ),
    path(
        "event/<slug:slug>/start",
        views.RegisterEventStart.as_view(),
        name="register_event_by_slug_start",
    ),
    path("misc/set_email_needed/<slug:slug>", views.set_email_needed, name="set_email_needed"),
    path("misc/set_email_needed/", views.set_email_needed, name="set_email_needed_no_slug"),
    path(
        "account/register/start",
        views.AccountRegisterStart.as_view(),
        name="register_account_start",
    ),
    path(
        "account/register",
        views.AccountRegisterWizardView.as_view(account_forms, condition_dict=account_conditions),
        name="register_account",
    ),
    path("events/feed", views.UpcomingEventsRSSFeed(), name="upcoming_events_rss_feed"),
    path("events/create", views.CreateEventView.as_view(), name="create_event"),
    path("events/manage", views.manage_events, name="manage_events"),
    path("vouchers/create", views.VoucherCreateView.as_view(), name="create_vouchers"),
    path(
        "vouchers/<int:pk>/delete", views.VoucherDeleteView.as_view(), name="delete_voucher_by_pk"
    ),
    path("vouchers/<int:pk>/edit", views.VoucherEditView.as_view(), name="edit_voucher_by_pk"),
    path("vouchers/<int:pk>/print", views.print_voucher, name="print_voucher_by_pk"),
    path("vouchers/", views.vouchers, name="vouchers"),
    path("event/lists/generate", views.generate_lists, name="generate_lists"),
    path(
        "event/registrations/<int:pk>/check_in",
        views.CheckInRegistration.as_view(),
        name="check_in_registration_by_pk",
    ),
    path(
        "event/registrations/<int:pk>/pay",
        views.MarkRegistrationPayed.as_view(),
        name="pay_registration_by_pk",
    ),
    path(
        "event/registrations/<int:pk>/retract",
        views.RetractRegistration.as_view(),
        name="retract_registration_by_pk",
    ),
    path(
        "event/registrations/<int:pk>",
        views.EventRegistrationDetailView.as_view(),
        name="registration_by_pk",
    ),
    path(
        "event/registrations/<int:pk>/edit",
        views.EventRegistrationEditView.as_view(),
        name="edit_registration_by_pk",
    ),
    path(
        "event/registrations/<int:pk>/delete",
        views.EventRegistrationDeleteView.as_view(),
        name="delete_registration_by_pk",
    ),
    path(
        "event/registrations/<int:pk>/notification",
        views.SendMailFromRegistration.as_view(),
        name="registration_notification_by_pk",
    ),
    path(
        "event/terms/list",
        views.TermListView.as_view(),
        name="terms",
    ),
    path(
        "event/terms/create",
        views.TermCreateView.as_view(),
        name="create_term",
    ),
    path(
        "event/terms/<int:pk>/edit",
        views.TermEditView.as_view(),
        name="edit_term_by_pk",
    ),
    path(
        "event/registrations/states/list",
        views.RegistrationStateListView.as_view(),
        name="registration_states",
    ),
    path(
        "event/registrations/states/create",
        views.RegistrationStateCreateView.as_view(),
        name="create_registration_state",
    ),
    path(
        "event/registrations/states/<int:pk>/edit",
        views.RegistrationStateEditView.as_view(),
        name="edit_registration_state_by_pk",
    ),
    path(
        "info_mailings/list",
        views.InfoMailingListView.as_view(),
        name="info_mailings",
    ),
    path(
        "info_mailings/create",
        views.InfoMailingCreateView.as_view(),
        name="create_info_mailing",
    ),
    path(
        "info_mailings/<int:pk>/edit",
        views.InfoMailingEditView.as_view(),
        name="edit_info_mailing_by_pk",
    ),
    path(
        "info_mailings/<int:pk>/delete",
        views.InfoMailingDeleteView.as_view(),
        name="delete_info_mailing_by_pk",
    ),
]
