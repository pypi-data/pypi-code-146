from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group

from .models import Volume, Action, UserRole

# BASIC
class ExplorerAdmin(AdminSite):
    site_title = 'Explorer Admin'
    site_header = 'Explorer Administration'
    index_title = 'Home Page'

explorer_admin = ExplorerAdmin(name='exploreradmin')

# VOLUMES
@admin.register(Volume, site=explorer_admin)
class VolumeAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'creation_date']
    list_display_links = ['name']
    list_filter = ['active', 'creation_date']
    ordering = ('-creation_date',)
    search_fields = ['name', 'active']
    fields = [('name', 'active'), 'path', 'creation_date']

# OPTION
@admin.register(Action, site=explorer_admin)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['name', 'creation_date']
    list_display_links = ['name']
    ordering = ('-creation_date',)
    fields = ['name', 'creation_date']

# USER ROLE
@admin.register(UserRole, site=explorer_admin)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'volume', 'creation_date']
    filter_horizontal = ['actions']
    list_filter = ['user', 'volume']
    ordering = ('-user',)
    search_fields = ['user', 'volume']