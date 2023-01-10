from django.contrib import admin
from django.urls import path

from .models import Champion
from .models import Product
from .models import Skin
from .utils.product import get_products_query_set
from .views import skins_download


@admin.register(Champion)
class ChampionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'roles',
        'lanes',
        'date_created',
        'date_modified',
    )

    search_fields = (
        'name',
    )


@admin.register(Skin)
class SkinAdmin(admin.ModelAdmin):

    change_list_template = 'shop/skins_change_list.html'

    list_display = (
        'id',
        'name',
        'champion',
        'tier',
        'value',
        'date_created',
        'date_modified',

    )

    search_fields = (
        'name',
        'champion__name',

    )

    list_filter = (
        'tier',
    )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('download/', skins_download)]
        return my_urls + urls


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''ProductAdmin class'''
    fields = (
        'username',
        'password',
        'level',
        'region',
        'blue_essence',
        'orange_essence',
        'mythic_essence',
        'all_skins',
        'skins',
        'owned_skins',
        'permanent_skins',
    )
    readonly_fields = (
        'all_skins',
    )
    list_display = (
        'username',
        'region',
        'discrete_level',
        'discrete_blue_essence',
        'orange_essence',
        'mythic_essence',
        'skin_count',
        'skin_score',
        'is_purchased',
        'date_created',
        'date_modified',
    )
    list_filter = (
        'date_modified',
        'discrete_level',
        'discrete_blue_essence',
        'region',
        'is_purchased',
    )
    search_fields = [
        'username',
        'region',
        'all_skins__name',
    ]
    filter_horizontal = ('skins', 'permanent_skins', 'owned_skins')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return get_products_query_set(qs)

    def skin_count(self, obj):
        return obj.skin_count

    def skin_score(self, obj):
        return obj.skin_score

    skin_score.admin_order_field = 'skin_score'
    skin_count.admin_order_field = 'skin_count'
