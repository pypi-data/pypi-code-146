from typing import Final, Iterable
from dataclass_to_diagram.models import state_machine
from .state_to_puml import state_to_puml
from .transition_to_puml import transition_to_puml

TEMPLATE: Final[
    str
] = """@startuml{options}{states}{transitions}

@enduml
"""


def _export_options(hide_empty_description: bool) -> str:
    options: list[str] = []
    if hide_empty_description:
        options.append("hide empty description")
    if not options:
        return ""
    return "\n\n{0}".format("\n".join(options))


def _export_states(states: Iterable[state_machine.State] | None) -> str:
    if not states:
        return ""
    states_str_list = [state_to_puml(state) for state in states]
    states_str = "\n".join(states_str_list)
    return "\n\n{0}".format(states_str)


def _export_transitions(
    transitions: Iterable[state_machine.Transition] | None,
) -> str:
    if not transitions:
        return ""
    transitions_list = [transition_to_puml(trans) for trans in transitions]
    transitions_str = "\n".join(transitions_list)
    return "\n\n{0}".format(transitions_str)


def diagram_to_puml(diagram: state_machine.Diagram) -> str:
    return TEMPLATE.format(
        options=_export_options(diagram.hide_empty_description),
        states=_export_states(diagram.states),
        transitions=_export_transitions(diagram.transitions),
    )
