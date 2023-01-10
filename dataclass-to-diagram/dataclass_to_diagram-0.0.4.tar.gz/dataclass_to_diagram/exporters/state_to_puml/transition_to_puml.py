from dataclass_to_diagram.models import state_machine

TEMPLATE: str = """{begin} --> {end}{options}{description}"""


def _export_description(description: str | None) -> str:
    if not description:
        return ""
    desc = description.replace("\n", "\\n")
    return " : {0}".format(desc)


def _export_options(is_history: bool, is_deep_history: bool) -> str:
    if is_history:
        return "[H]"
    if is_deep_history:
        return "[H*]"
    return ""


def transition_to_puml(transition: state_machine.Transition) -> str:
    return TEMPLATE.format(
        begin=transition.begin.alias,
        end=transition.end.alias,
        options=_export_options(
            is_history=transition.option == "history",
            is_deep_history=transition.option == "deep_history",
        ),
        description=_export_description(transition.description),
    )
