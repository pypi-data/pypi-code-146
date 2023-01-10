from django.contrib import admin

from config.config import JConfig
# 引入用户平台
from .models import *

config = JConfig()


# Register your models here.


class BaseInfoAdmin(admin.ModelAdmin):
    # fields = ('user_name', 'full_name', 'platform', 'platform_uid', 'phone', 'email', 'wechat', 'user_info')
    fields = ('id', 'user_name', 'full_name', 'nickname', 'phone', 'email', 'wechat_openid', 'user_info', 'register_time')
    list_display = (
        'id', 'user_name', 'full_name', 'nickname', 'phone', 'email', 'wechat_openid', 'user_info', 'register_time')
    search_fields = ('user_name', 'full_name', 'nickname', 'phone',)
    list_filter = []
    readonly_fields = ['id']


class AuthAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'password', 'salt', 'algorithm', 'token', 'ticket', 'create_time', 'update_time')
    list_display = ('user', 'password', 'token', 'create_time', 'update_time',)
    search_fields = ('user', 'create_time')
    list_filter = ['user']
    readonly_fields = ['id', 'create_time', 'update_time']

    # def platform(self, obj):
    #     return obj.platform


class DetailInfoAdmin(admin.ModelAdmin):
    fields = (
        'id', 'user', 'real_name', 'sex', 'birth', 'tags', 'signature', 'avatar', 'cover', 'language', 'region_code',
        'more',
        'field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6', 'field_7', 'field_8', 'field_9',
        'field_10', 'field_11', 'field_12', 'field_13', 'field_14', 'field_15'
    )
    list_display = ('user', 'real_name', 'sex', 'birth', 'tags', 'avatar', 'cover', 'language', 'region_code')
    readonly_fields = ['id']


class ExtendFieldAdmin(admin.ModelAdmin):
    fields = ('id', 'field', 'field_index', 'description', 'type', 'config', 'default', 'sort')
    list_display = ('field', 'field_index', 'description', 'type', 'config', 'default', 'sort')
    readonly_fields = ['id']


class AccessLogAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'ip', 'create_time', 'client_info', 'more',)
    list_display = ('user', 'ip', 'create_time', 'client_info',)
    readonly_fields = ['id', 'create_time']


class HistoryAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'field', 'old_value', 'new_value', 'create_time',)
    list_display = ('user', 'field', 'old_value', 'new_value', 'create_time',)
    readonly_fields = ['id', 'create_time']


class RestrictRegionAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'region_code',)
    list_display = ('user', 'region_code',)
    readonly_fields = ['id']


class PlatformAdmin(admin.ModelAdmin):
    fields = ('platform_id', 'platform_name')
    list_display = ('platform_id', 'platform_name')
    search_fields = ('platform_id', 'platform_name')


class PlatformsToUsersAdmin(admin.ModelAdmin):
    fields = ('id', 'platform', 'platform_user_id',)
    list_display = ('platform', 'platform_user_id',)
    readonly_fields = ['id']


# class PermissionAdmin(admin.ModelAdmin):
#     fields = ('permission_id', 'permission_name',)
#     list_display = ('permission_id', 'permission_name',)


# class PermissionValueAdmin(admin.ModelAdmin):
#     fields = ('id', 'permission', 'module', 'feature', 'permission_value', 'type',
#               'relate_value', 'config', 'is_enable', 'is_system', 'is_ban', 'ban_view', 'ban_edit', 'ban_add',
#               'ban_delete',
#               'description')
#     list_display = ('permission', 'permission_value', 'type', 'is_system', 'is_ban',)
#     readonly_fields = ['id']


# class GroupAdmin(admin.ModelAdmin):
#     fields = ('id', 'group', 'parent_group', 'description')
#     list_display = ('id', 'group', 'parent_group', 'description')
#     readonly_fields = ['id']


class ContactBookAdmin(admin.ModelAdmin):
    fields = ('id', 'user_id', 'friend', 'phone', 'phones', 'telephone', 'telephones',
              'email', 'qq', 'address', 'more', 'remarks')
    list_display = ('id', 'user_id', 'friend', 'phone', 'phones', 'telephone', 'telephones',
                    'email', 'qq', 'address', 'more', 'remarks')
    readonly_fields = ['id']


class UserSsoServeAdmin(admin.ModelAdmin):
    fields = ('id', 'sso_code', 'sso_name', 'sso_url', 'description')
    list_display = ('id', 'sso_code', 'sso_name', 'sso_url', 'description')
    readonly_fields = ['id']


class UserSsoToUserAdmin(admin.ModelAdmin):
    fields = ('id', 'sso_serve', 'user', 'sso_unicode', 'sso_ticket', 'app_id')
    list_display = ('id', 'sso_serve', 'user', 'sso_unicode', 'sso_ticket', 'app_id')
    readonly_fields = ['id']


class UserRelateTypeAdmin(admin.ModelAdmin):
    fields = ("id", "relate_key", "relate_name", "description",)
    list_display = ("id", "relate_key", "relate_name", "description",)
    readonly_fields = ['id']


class UserRelateToUserAdmin(admin.ModelAdmin):
    fields = ("id", "user", "with_user", "user_relate_type",)
    list_display = ("id", "user", "with_user", "user_relate_type",)
    readonly_fields = ['id']


admin.site.register(BaseInfo, BaseInfoAdmin)
admin.site.register(Auth, AuthAdmin)
admin.site.register(DetailInfo, DetailInfoAdmin)
admin.site.register(AccessLog, AccessLogAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(RestrictRegion, RestrictRegionAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(PlatformsToUsers, PlatformsToUsersAdmin)
# admin.site.register(Permission, PermissionAdmin)
# admin.site.register(PermissionValue, PermissionValueAdmin)
# admin.site.register(Group, GroupAdmin)
admin.site.register(ContactBook, ContactBookAdmin)
admin.site.register(ExtendField, ExtendFieldAdmin)
admin.site.register(UserSsoServe, UserSsoServeAdmin)
admin.site.register(UserSsoToUser, UserSsoToUserAdmin)
admin.site.register(UserRelateType, UserRelateTypeAdmin)
admin.site.register(UserRelateToUser, UserRelateToUserAdmin)
