from extras.plugins import PluginMenuItem
from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

risk_buttons = [
    PluginMenuButton(
        link='plugins:users_and_computers:risk_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]
risk_rel_buttons = [
    PluginMenuButton(
        link='plugins:users_and_computers:riskrelation_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]

menu_items = (
    PluginMenuItem(
        link='plugins:users_and_computers:risk_list',
        link_text='AD Users',
        buttons=risk_buttons
    ),
    PluginMenuItem(
        link='plugins:users_and_computers:riskrelation_list',
        link_text='Workstations',
        buttons=risk_rel_buttons
    ),
)
