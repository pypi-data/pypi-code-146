from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *


@admin.register(PWASettings)
class PWASettingsAdmin(TranslationAdmin):
    pass
