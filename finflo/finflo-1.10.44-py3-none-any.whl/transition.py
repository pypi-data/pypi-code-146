import json
from .models import (
    SignList,
    TransitionManager,
    Action,
    workevents,
    workflowitems,
    Flowmodel,
)
from django.core import serializers as core_serializers
from .middleware import get_current_user
from .exception import (
    ModelNotFound,
    TransitionNotAllowed,
    ReturnModelNotFound,
)
from django.db.models import Q
from django.conf import settings
from collections import deque
from django.apps import apps
from django.forms.models import model_to_dict


####################################################
#############       CORE     #######################
####################################################


class FinFlotransition:

    # BASE CONSTRUCTORS #

    def __init__(self,type,t_id,action=None,party=None,source=None,interim=None,target=None,from_party=None,to_party=None,) -> str:
        self.type = type
        self.t_id = t_id
        self.party = party.upper() if party else None
        self.action = action.upper() if action else None
        self.source = source or None
        self.interim = interim or None
        self.target = target or None
        self.from_party = from_party or None
        self.to_party = to_party or None
        gets_current_Action = None
        gets_return_action = self.gets_default_return_action()
        if action:
            if action == gets_return_action.description:
                self.return_transition()
            else:
                self.transition()
        else:
            self.manualtransitions()
        # return None

    def __repr__(self):
        return f"the id is {self.t_id} and type is {self.type}"

    def __str__(self):
        return f"the id is {self.t_id} and type is {self.type}"

    # GETS THE ALL MODEL VALUE FOR TRANSITION #

    def gets_base_action(self):
        try:
            return Action.objects.get(description=self.action, model__description=self.type)
        except:
            raise ModelNotFound()

    # RETURN ACTION
    def gets_default_return_action(self):
        try:
            return Action.objects.get(id=1)
        except:
            raise ReturnModelNotFound()

    # GETS WORKFLOW MODEL ID #
    def gets_wf_item(self, model):
        ws = workflowitems.objects.get(transitionmanager=model)
        return ws

    # GETS TRANSITION MANAGER
    def gets_base_model(self):
        try:
            return TransitionManager.objects.get(type=self.type, t_id=self.t_id)
        except Exception:
            ModelNotFound()

    # GETS ALL ACTION
    def gets_all_models(self):
        try:
            gets_model = TransitionManager.objects.get(type__icontains=self.type, t_id=self.t_id)
            gets_flows = Flowmodel.objects.get(description__icontains=self.type)
            gets_action = Action.objects.get(
                Q(model=gets_flows.id) | Q(model=None),
                description=self.action,
                party=self.party or None,
            )
            gets_wf = self.gets_wf_item(gets_model.id)
            sign_lists = []
            try:
                for item in SignList.objects.all():
                    sign_lists.append(item.name)
                    if item.name == gets_action.stage_required.name:
                        break
                next_avail_trans = sign_lists[gets_model.sub_sign :]
                next_avail_trans_value = deque(next_avail_trans)
                next_avail_trans_value.popleft()
                next_states = list(next_avail_trans_value)
                next_avail_Transition = {"values": next_states}
            except Exception:
                next_avail_Transition = None
            return (
                gets_model,
                gets_action,
                gets_flows,
                gets_wf,
                sign_lists,
                next_avail_Transition,
            )
        except:
            raise ModelNotFound()


    def return_transition(self):

        overall_model = self.gets_all_models()
        obj, created = workflowitems.objects.update_or_create(
            transitionmanager=overall_model[0] or overall_model[0].id,
            defaults={
                "initial_state": overall_model[1].from_state.description
                if overall_model[1].from_state
                else overall_model[3].initial_state,
                "interim_state": overall_model[1].to_state.description,
                "final_state": overall_model[1].to_state.description,
                "action": self.action,
                "record_datas": self.get_record_datas(),
                "subaction": self.action,
                "previous_action": overall_model[3].action,
                "next_available_transitions": None,
                "model_type": self.type,
                "event_user": get_current_user(),
                "final_value": True,
                "current_from_party": overall_model[1].from_party or self.from_party,
                "current_to_party": overall_model[1].to_party or self.to_party,
            },
        )
        workevents.objects.create(
            workflowitems=overall_model[3],
            event_user=get_current_user(),
            initial_state=overall_model[1].from_state.description
            if overall_model[1].from_state
            else overall_model[3].initial_state,
            final_value=True,
            record_datas=self.get_record_datas(),
            interim_state=overall_model[1].to_state.description,
            final_state=overall_model[1].to_state.description,
            action=self.action,
            subaction=self.action,
            type=self.type,
            from_party=overall_model[1].from_party or self.from_party,
            to_party=overall_model[1].to_party or self.to_party,
        )
        overall_model[0].sub_sign = 0
        overall_model[0].in_progress = False
        overall_model[0].save()

    def get_record_datas(self):
        overall_model = self.gets_base_model()
        try:
            work_model = settings.FINFLO["WORK_MODEL"]
            for iter in work_model:
                gets_model = apps.get_model(iter)
                query_data = gets_model.objects.filter(id=overall_model.t_id)
                base_serialized_Data = core_serializers.serialize("json", query_data)
                if query_data.exists() and (gets_model._meta.db_table == overall_model.type):
                    break
                continue
            return {"values": json.loads(base_serialized_Data)}
        except Exception:
            return {"values": None}




    # MANUAL TRANSITION WITH SOURCE , INTERIM , AND TARGET STATES

    def manualtransitions(self):
        try:
            queryset = self.gets_base_model()
            obj, created = workflowitems.objects.update_or_create(
                transitionmanager=queryset,
                defaults={
                    "initial_state": self.source,
                    "interim_state": self.interim,
                    "final_state": self.target,
                    "next_available_transitions": None,
                    "record_datas": self.get_record_datas(),
                    "model_type": self.type,
                    "event_user": get_current_user(),
                    "current_from_party": self.from_party,
                    "current_to_party": self.to_party,
                    "final_value": True,
                },
            )
            workevents.objects.create(
                workflowitems=obj,
                event_user=get_current_user(),
                initial_state=self.source,
                interim_state=self.interim,
                final_state=self.target,
                type=self.type,
                record_datas=self.get_record_datas(),
                from_party=self.from_party,
                to_party=self.to_party,
                final_value=True,
            )
        except Exception:
            return None




    ## CORE TRANSITION ###

    def transition(self):

        overall_model = self.gets_all_models()

        if overall_model[0] is not None:

            def Transition_Handler():

                if len(overall_model[4]) == overall_model[0].sub_sign:
                    return
                try:
                    ws = workflowitems.objects.update_or_create(
                        transitionmanager=overall_model[0] or overall_model[0].id,
                        defaults={
                            "initial_state": overall_model[1].from_state.description,
                            "interim_state": overall_model[4][
                                1 + overall_model[0].sub_sign
                            ],
                            "final_state": overall_model[1].to_state.description,
                            "next_available_transitions": overall_model[5],
                            "action": self.action,
                            "subaction": overall_model[4][overall_model[0].sub_sign],
                            "model_type": self.type,
                            "record_datas": self.get_record_datas(),
                            "event_user": get_current_user(),
                            "current_from_party": overall_model[1].from_party or self.from_party,
                            "current_to_party": overall_model[1].to_party or self.to_party,
                        },
                    )
                    workevents.objects.create(
                        workflowitems=overall_model[3],
                        event_user=get_current_user(),
                        initial_state=overall_model[1].from_state.description,
                        interim_state=overall_model[4][1 + overall_model[0].sub_sign],
                        record_datas=self.get_record_datas(),
                        final_state=overall_model[1].to_state.description,
                        action=self.action,
                        subaction=self.action,
                        type=self.type,
                        from_party=overall_model[1].from_party or self.from_party,
                        to_party=overall_model[1].to_party or self.to_party,
                    )
                    overall_model[0].sub_sign += 1
                    overall_model[0].in_progress = True
                    overall_model[0].save()
                except Exception:
                    ws = workflowitems.objects.update_or_create(
                        transitionmanager=overall_model[0] or overall_model[0].id,
                        defaults={
                            "initial_state": overall_model[1].from_state.description,
                            "interim_state": overall_model[1].to_state.description,
                            "final_state": overall_model[1].to_state.description,
                            "action": self.action,
                            "next_available_transitions": None,
                            "subaction": self.action,
                            "model_type": self.type,
                            "record_datas": self.get_record_datas(),
                            "event_user": get_current_user(),
                            "current_from_party": overall_model[1].from_party or self.from_party,
                            "current_to_party": overall_model[1].to_party or self.to_party,
                            "final_value": True,
                        },
                    )
                    workevents.objects.create(
                        workflowitems=overall_model[3],
                        event_user=get_current_user(),
                        initial_state=overall_model[1].from_state.description,
                        interim_state=overall_model[1].to_state.description,
                        record_datas=self.get_record_datas(),
                        final_state=overall_model[1].to_state.description,
                        action=self.action,
                        subaction=self.action,
                        type=self.type,
                        from_party=overall_model[1].from_party or self.from_party,
                        to_party=overall_model[1].to_party or self.to_party,
                        final_value=True,
                    )
                    overall_model[0].sub_sign = 0
                    overall_model[0].in_progress = False
                    overall_model[0].save()

            return Transition_Handler()
        else:
            raise TransitionNotAllowed()


class ReverseTransition:
    pass
