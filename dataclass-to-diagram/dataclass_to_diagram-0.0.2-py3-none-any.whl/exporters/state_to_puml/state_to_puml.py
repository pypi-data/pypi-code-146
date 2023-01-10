from typing import Iterable

from dataclass_to_diagram.models import state_machine

from ..shared.increase_indent import increase_indent

TEMPLATE: str = """state "{name}" as {alias}{internal_states}{decription}"""
START: str = "state {alias} <<start>>"
END: str = "state {alias} <<end>>"
FORK: str = "state {alias} <<fork>>"
JOIN: str = "state {alias} <<join>>"
CHOICE: str = "state {alias} <<choice>>"


def _export_internal_states(
    internal_states: Iterable[state_machine.State] | None,
) -> str:
    if not internal_states:
        return ""
    internal_states_list = [
        state_to_puml(int_state) for int_state in internal_states
    ]
    internal_states_list = list(
        filter(lambda state: state, internal_states_list),
    )
    internal_states_str = increase_indent("\n".join(internal_states_list))
    return " {{\n{0}\n}}".format(internal_states_str)


DESC_LINE_TEMPLATE: str = "{alias} : {description_line}"


def _export_description(
    state_alias: int,
    description: str | None,
) -> str:
    if not description:
        return ""
    desc_lines = description.split("\n")
    desc_lines_format = [
        DESC_LINE_TEMPLATE.format(
            alias=state_alias,
            description_line=line,
        )
        for line in desc_lines
    ]
    desc_lines_str = "\n".join(desc_lines_format)
    return "\n{0}".format(desc_lines_str)


def state_to_puml(state: state_machine.State) -> str:
    match state:
        case state_machine.StateChoice():
            return CHOICE.format(alias=state.alias)
        case state_machine.StateEnd():
            return END.format(alias=state.alias)
        case state_machine.StateFork():
            return FORK.format(alias=state.alias)
        case state_machine.StateJoin():
            return JOIN.format(alias=state.alias)
        case state_machine.StateStart():
            return START.format(alias=state.alias)
        case state_machine.State():
            return TEMPLATE.format(
                name=state.name,
                alias=state.alias,
                internal_states=_export_internal_states(state.internal_states),
                decription=_export_description(state.alias, state.description),
            )
