from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Vassal


@admin.action(description=_("Enable selected Emperor's Vassals"))
def enabled(modeladmin, request, queryset):
    queryset.update(enabled='1')


@admin.action(description=_("Disable selected Emperor's Vassals"))
def disabled(modeladmin, request, queryset):
    queryset.update(enabled='0')


class VassalFields:
    list_display = ('title', 'extension', 'updated', 'created', 'enabled', 'ts')
    search_fields = ('title',)
    list_filter = ('enabled', 'created', 'extension')


@admin.register(Vassal)
class VassalAdmin(VassalFields, admin.ModelAdmin):
    actions = (enabled, disabled)
