from modeltranslation.translator import translator, TranslationOptions
from .models import *


class PWASettingsTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
    )

translator.register(PWASettings, PWASettingsTranslationOptions)
