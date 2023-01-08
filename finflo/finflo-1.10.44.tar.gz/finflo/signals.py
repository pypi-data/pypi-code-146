import contextlib
from django import dispatch
from django.db.models.signals import post_save, post_delete
from .exception import DefaultsNotFoundError, PartyLengthError
from .middleware import get_current_user
from .models import States, TransitionManager, workevents, workflowitems
from django.conf import settings
from .transition import FinFlotransition
from .compatability import check_version_compatibility


# MAIN SIGNAL RECEIVER FOR TRANSITION HANDLING - 4/8/2022 by anand

Base_link = "https://pypi.org/project/finflo/"


# CORE LIST ITERATED FROM THE DEFAULT SETTINGS -- PRODUCTION : 27/10/2022
try:
    check_version_compatibility()
    WORK_MODEL_SENDER = list(settings.FINFLO["WORK_MODEL"])
    PARTY_MODEL_SENDER = list(settings.FINFLO["PARTY_MODEL"])
except:
    raise DefaultsNotFoundError(
        "unable to find WORK_MODEL and PARTY_MODEL in your settings.py file , \
        check the documentation for more details",
        Base_link,
    )


# CUSTOM MULTIPLE RECEIVER SIGNALS


def finflo_receiver(signal, senders, **kwargs):
    def decorator(receiver_func):
        for sender in senders:
            if isinstance(signal, (list, tuple)):
                for s in signal:
                    s.connect(receiver_func, sender=sender, **kwargs)
            else:
                signal.connect(receiver_func, sender=sender, **kwargs)
        return receiver_func

    return decorator


# MULTIPLE RECEIVER MODEL WITH MULTIPLE SENDERS

#### CREATER

## A
@finflo_receiver(post_save, senders=WORK_MODEL_SENDER)
def creates_finflo_work_models(sender, instance, created, **kwargs):
    if created:
        model = sender._meta.db_table
        states = States.objects.get(id=1)
        obj = TransitionManager.objects.create(type=model, t_id=instance.id)
        gets_transition = FinFlotransition(t_id=obj.id, type=model)
        obj2 = workflowitems.objects.create(
            transitionmanager=obj,
            model_type=model,
            record_datas=gets_transition.get_record_datas(),
            initial_state=states.description,
            interim_state=states.description,
            final_state=states.description,
        )
        workevents.objects.create(
            workflowitems=obj2,
            type=model,
            record_datas=gets_transition.get_record_datas(),
            initial_state=states.description,
            interim_state=states.description,
            final_state=states.description,
        )


# POST DELETE

## A
@finflo_receiver(post_delete, senders=WORK_MODEL_SENDER)
def delete(sender, instance, **kwargs):
    TransitionManager.objects.filter(type=sender._meta.db_table, t_id=instance.id).delete()
