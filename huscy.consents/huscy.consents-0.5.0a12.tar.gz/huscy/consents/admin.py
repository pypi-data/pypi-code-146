from django.contrib import admin

from huscy.consents import models


class ConsentAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name'


class ConsentCategoryAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name'


class ConsentFileAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = 'consent', 'created_at', 'filehandle'
    readonly_fields = 'created_at',


admin.site.register(models.Checkbox)
admin.site.register(models.Consent, ConsentAdmin)
admin.site.register(models.ConsentCategory, ConsentCategoryAdmin)
admin.site.register(models.ConsentFile, ConsentFileAdmin)
admin.site.register(models.Paragraph)
admin.site.register(models.TemplateTextFragment)
