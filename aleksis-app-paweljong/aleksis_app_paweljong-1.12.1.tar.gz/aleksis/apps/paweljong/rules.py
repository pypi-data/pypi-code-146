import rules

from aleksis.core.util.predicates import (
    has_any_object,
    has_global_perm,
    has_object_perm,
    has_person,
)

from .models import Event, EventRegistration, Terms, Voucher
from .predicates import (
    is_event_published,
    is_organiser,
    is_own_registration,
    is_own_voucher,
    is_participant,
)

## Vouchers

# View vouchers
view_vouchers_predicate = has_person & (
    has_global_perm("paweljong.view_voucher") | has_any_object("paweljong.view_voucher", Voucher)
)
rules.add_perm("paweljong.view_vouchers_rule", view_vouchers_predicate)

# View voucher
view_voucher_predicate = has_person & (
    is_own_voucher
    | has_global_perm("paweljong.view_voucher")
    | has_object_perm("paweljong.view_voucher")
)
rules.add_perm("paweljong.view_voucher_rule", view_voucher_predicate)

# Edit voucher
change_voucher_predicate = has_person & (
    has_global_perm("paweljong.change_voucher") | has_object_perm("paweljong.change_voucher")
)
rules.add_perm("paweljong.change_voucher_rule", change_voucher_predicate)

# Delete voucher
delete_voucher_predicate = has_person & (
    has_global_perm("paweljong.delete_voucher") | has_object_perm("paweljong.delete_voucher")
)
rules.add_perm("paweljong.delete_voucher_rule", delete_voucher_predicate)

# Create vouchers
create_vouchers_predicate = has_person & (
    has_global_perm("paweljong.create_voucher")
    | has_any_object("paweljong.create_voucher", Voucher)
)
rules.add_perm("paweljong.create_vouchers_rule", create_vouchers_predicate)

## Events

# View events
view_events_predicate = has_person & (
    has_global_perm("paweljong.view_event") | has_any_object("paweljong.view_event_rule", Event)
)
rules.add_perm("paweljong.view_events_rule", view_events_predicate)

# Edit event
change_event_predicate = has_person & (
    has_global_perm("paweljong.change_event")
    | has_object_perm("paweljong.change_event")
    | is_organiser
)
rules.add_perm("paweljong.change_event_rule", change_event_predicate)

# Edit events
change_events_predicate = has_person & (
    has_global_perm("paweljong.change_event") | has_any_object("paweljong.change_event_rule", Event)
)
rules.add_perm("paweljong.change_events_rule", change_events_predicate)

# Checkpoint
checkpoint_predicate = change_event_predicate
rules.add_perm("paweljong.event_checkpoint_rule", checkpoint_predicate)

# View event
view_event_predicate = (
    is_event_published | (has_person & is_organiser) | has_object_perm("paweljong.view_event")
)
rules.add_perm("paweljong.view_event_rule", view_event_predicate)

# Event organiser view
view_event_detail_predicate = has_person & is_organiser
rules.add_perm("paweljong.view_event_detail_rule", view_event_detail_predicate)

# Delete event
delete_event_predicate = has_person & (
    has_global_perm("paweljong.delete_event") | has_object_perm("paweljong.delete_event")
)
rules.add_perm("paweljong.delete_event_rule", delete_event_predicate)

# Create events
create_events_predicate = has_person & (
    has_global_perm("paweljong.create_event") | has_any_object("paweljong.create_event", Event)
)
rules.add_perm("paweljong.create_events_rule", create_events_predicate)

## Registrations

# View registration
view_registration_predicate = has_person & (
    has_global_perm("paweljong.view_eventregistration")
    | has_object_perm("paweljong.view_eventregistration")
    | is_organiser
    | is_own_registration
)
rules.add_perm("paweljong.view_registration_rule", view_registration_predicate)

# View registrations
view_registrations_predicate = has_person & (
    has_global_perm("paweljong.view_eventregistration")
    | has_any_object("paweljong.view_registration_rule", EventRegistration)
)
rules.add_perm("paweljong.view_registrations_rule", view_registrations_predicate)

# Delete registration
delete_registration_predicate = has_person & (
    has_global_perm("paweljong.delete_eventregistration")
    | has_object_perm("paweljong.delete_eventregistration")
)
rules.add_perm("paweljong.delete_registration_rule", delete_registration_predicate)

# Change registration
change_registration_predicate = has_person & (
    has_global_perm("paweljong.change_eventregistration")
    | has_object_perm("paweljong.change_eventregistration")
    | is_organiser
)
rules.add_perm("paweljong.change_registration_rule", change_registration_predicate)

## Terms

# View terms
view_terms_predicate = has_person & (
    has_global_perm("paweljong.view_term") | has_any_object("paweljong.view_term", Terms)
)
rules.add_perm("paweljong.view_terms_rule", view_terms_predicate)

# View term
view_term_predicate = has_person & (
    has_global_perm("paweljong.view_term") | has_object_perm("paweljong.view_term")
)
rules.add_perm("paweljong.view_term_rule", view_term_predicate)

# Delete term
delete_term_predicate = has_person & (
    has_global_perm("paweljong.delete_eventterm") | has_object_perm("paweljong.delete_eventterm")
)
rules.add_perm("paweljong.delete_term_rule", delete_term_predicate)

# Change term
change_term_predicate = has_person & (
    has_global_perm("paweljong.change_eventterm") | has_object_perm("paweljong.change_eventterm")
)
rules.add_perm("paweljong.change_term_rule", change_term_predicate)

# Create terms
create_terms_predicate = has_person & (
    has_global_perm("paweljong.create_term") | has_any_object("paweljong.create_term", Event)
)
rules.add_perm("paweljong.create_terms_rule", create_terms_predicate)

## Info mailings

# View info_mailings
view_info_mailings_predicate = has_person & (
    has_global_perm("paweljong.view_info_mailing")
    | has_any_object("paweljong.view_info_mailing", Terms)
)
rules.add_perm("paweljong.view_info_mailings_rule", view_info_mailings_predicate)

# View info_mailing
view_info_mailing_predicate = has_person & (
    has_global_perm("paweljong.view_info_mailing") | has_object_perm("paweljong.view_info_mailing")
)
rules.add_perm("paweljong.view_info_mailing_rule", view_info_mailing_predicate)

# Delete info_mailing
delete_info_mailing_predicate = has_person & (
    has_global_perm("paweljong.delete_eventinfo_mailing")
    | has_object_perm("paweljong.delete_eventinfo_mailing")
)
rules.add_perm("paweljong.delete_info_mailing_rule", delete_info_mailing_predicate)

# Change info_mailing
change_info_mailing_predicate = has_person & (
    has_global_perm("paweljong.change_eventinfo_mailing")
    | has_object_perm("paweljong.change_eventinfo_mailing")
)
rules.add_perm("paweljong.change_info_mailing_rule", change_info_mailing_predicate)

# Create info_mailings
create_info_mailings_predicate = has_person & (
    has_global_perm("paweljong.create_info_mailing")
    | has_any_object("paweljong.create_info_mailing", Event)
)
rules.add_perm("paweljong.create_info_mailings_rule", create_info_mailings_predicate)

## Registration states

# View registration_states
view_registration_states_predicate = has_person & (
    has_global_perm("paweljong.view_registration_state")
    | has_any_object("paweljong.view_registration_state", Terms)
)
rules.add_perm("paweljong.view_registration_states_rule", view_registration_states_predicate)

# View registration_state
view_registration_state_predicate = has_person & (
    has_global_perm("paweljong.view_registration_state")
    | has_object_perm("paweljong.view_registration_state")
)
rules.add_perm("paweljong.view_registration_state_rule", view_registration_state_predicate)

# Delete registration_state
delete_registration_state_predicate = has_person & (
    has_global_perm("paweljong.delete_eventregistration_state")
    | has_object_perm("paweljong.delete_eventregistration_state")
)
rules.add_perm("paweljong.delete_registration_state_rule", delete_registration_state_predicate)

# Change registration_state
change_registration_state_predicate = has_person & (
    has_global_perm("paweljong.change_eventregistration_state")
    | has_object_perm("paweljong.change_eventregistration_state")
)
rules.add_perm("paweljong.change_registration_state_rule", change_registration_state_predicate)

# Create registration_states
create_registration_states_predicate = has_person & (
    has_global_perm("paweljong.create_registration_state")
    | has_any_object("paweljong.create_registration_state", Event)
)
rules.add_perm("paweljong.create_registration_states_rule", create_registration_states_predicate)

# View menu
can_view_menu_predicate = has_person & (
    view_registrations_predicate
    | view_info_mailings_predicate
    | view_terms_predicate
    | view_vouchers_predicate
    | view_events_predicate
    | view_registration_states_predicate
)
rules.add_perm("paweljong.view_menu", can_view_menu_predicate)

can_retract_registration_predicate = has_person & (is_organiser)
rules.add_perm("paweljong.can_retract_registration_rule", can_retract_registration_predicate)

can_view_terms_predicate = has_person & (is_participant)
rules.add_perm("paweljong.can_view_terms_rule", can_view_terms_predicate)

can_mark_payment_as_payed_predicate = has_person & (is_organiser)
rules.add_perm("paweljong.mark_payment_payed_rule", can_mark_payment_as_payed_predicate)
