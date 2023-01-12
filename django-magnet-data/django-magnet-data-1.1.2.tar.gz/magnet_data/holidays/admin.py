# django
from django.contrib import admin

from holidays.models import Holiday


class HolidayAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "country_code")


admin.site.register(Holiday, HolidayAdmin)
