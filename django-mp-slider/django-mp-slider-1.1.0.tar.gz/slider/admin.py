
from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

from slider.models import SliderImage


@admin.register(SliderImage)
class SliderImageAdmin(OrderedModelAdmin):

    list_display = ['id', 'title', 'file', 'url']
    fields = ['title', 'file', 'url']
    list_display_links = ['id', 'title']
