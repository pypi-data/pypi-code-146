from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.contrib.modeladmin.options import modeladmin_register

from .admin import VassalFields
from .models import Vassal


class VassalModelAdmin(VassalFields, ModelAdmin):
    model = Vassal
    menu_icon = 'cogs'
    menu_order = 800
    add_to_settings_menu = True


modeladmin_register(VassalModelAdmin)
