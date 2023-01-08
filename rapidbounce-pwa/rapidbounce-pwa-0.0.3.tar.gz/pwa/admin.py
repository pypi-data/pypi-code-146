from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from reversion.admin import VersionAdmin
from .models import *


@admin.register(PWASettings)
class PWASettingsAdmin(TranslationAdmin, VersionAdmin):
    pass
