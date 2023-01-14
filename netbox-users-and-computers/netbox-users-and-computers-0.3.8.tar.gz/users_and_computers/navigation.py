"""
from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:users_and_computers:mylink',
        link_text='MyLink',
        buttons=(
            PluginMenuButton('home', 'Button A', 'mdi mdi-plus-thick-info', ButtonColorChoices.BLUE),
        )
    ),
)
"""
