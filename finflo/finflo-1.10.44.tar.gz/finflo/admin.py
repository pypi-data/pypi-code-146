from django.contrib import admin
from .models import Action, Flowmodel, Party, States, TransitionManager , workevents , workflowitems , SignList 
# Register your models here.
from django.contrib import messages
from django.utils.translation import ngettext
from django.conf import settings

@admin.action(description='Reset selected items')
def make_in_progress_to_false(modeladmin, request, queryset):
    queryset.update(in_progress = False , sub_sign = 0)


class TransitionModeladmin(admin.ModelAdmin):
    list_display = ("t_id", "type", "in_progress")
    actions = [make_in_progress_to_false]


class CustomActionAdminModel(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return obj is None or obj.pk != 1

class customadminforsign(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False
    

admin.site.register(Flowmodel)
admin.site.register(TransitionManager,TransitionModeladmin)
admin.site.register(Action , CustomActionAdminModel )
admin.site.register(States)
admin.site.register(Party)
admin.site.register(SignList , customadminforsign)
admin.site.register(workflowitems)
admin.site.register(workevents)