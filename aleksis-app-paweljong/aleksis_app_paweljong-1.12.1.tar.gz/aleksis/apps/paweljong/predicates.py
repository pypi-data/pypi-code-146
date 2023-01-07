from typing import Union

from django.contrib.auth import get_user_model

from rules import predicate

from .models import Event, EventRegistration, Voucher

User = get_user_model()


@predicate
def is_own_voucher(user: User, obj: Voucher) -> bool:
    """Predicate which checks if the voucher belongs to the user."""
    return obj.person == user.person


@predicate
def is_own_registration(user: User, obj: EventRegistration) -> bool:
    """Predicate which checks if the registration belongs to the user."""
    return obj.person == user.person


@predicate
def is_organiser(user: User, obj: Union[Event, EventRegistration]) -> bool:
    """Predicate which checks if the user is an organiser."""
    if isinstance(obj, EventRegistration):
        event = obj.event
    elif isinstance(obj, Event):
        event = obj
    else:
        raise TypeError("This predicate can only check Event and EventRegistration.")

    return user.person in event.linked_group.owners.all()


@predicate
def is_event_published(user: User, obj: EventRegistration) -> bool:
    """Predicate which checks if the event is published."""
    return obj.published


@predicate
def is_participant(user: User, obj: Event) -> bool:
    """Predicate which checks if the user is member of the event."""
    return user.person in obj.linked_group.members.all()
