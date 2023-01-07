from django.utils.translation import gettext_lazy as _

from aleksis.core.data_checks import DataCheck, IgnoreSolveOption, SolveOption


class SyncEventMembers(SolveOption):
    name = "sync_event_members"
    verbose_name = _("Sync members")

    @classmethod
    def solve(cls, check_result: "DataCheckResult"):
        event = check_result.related_object
        event.sync_group_members()
        check_result.delete()


class EventMembersSyncDataCheck(DataCheck):
    name = "event_members_sync"
    verbose_name = _("Ensure that all registered persons are member of the linked group")
    problem_name = _("Event members are out of sync with registrations!")
    solve_options = {
        IgnoreSolveOption.name: IgnoreSolveOption,
        SyncEventMembers.name: SyncEventMembers,
    }

    @classmethod
    def check_data(cls):
        from .models import Event

        async_events = []
        for event in Event.objects.all():
            if not set(event.linked_group.members.values_list("id", flat=True)) == set(
                event.registrations.filter(retracted=False).values_list("person", flat=True)
            ):
                async_events.append(event)

        for event in async_events:
            cls.register_result(event)
