from django.contrib import admin

from config.config import JConfig
from .models import Thread, ThreadStatistic
from .models import ThreadExtendData
from .models import ThreadExtendField
from .models import ThreadImageAuth
from .models import ThreadShow, ThreadClassify, ThreadCategory
from .models import ThreadTag, ThreadTagMapping

config = JConfig()

# @admin.register(ThreadAuth)
# class ThreadAuthAdmin(admin.ModelAdmin):
#     list_display = ('id', 'value')
#     search_fields = ('id', 'value')
#     fields = ('id', 'value',)
#     readonly_fields = ('id',)

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'is_deleted', 'category_id', 'classify_id', 'show', 'user_id', 'with_user_id', 'short_title',
        'short_subtitle', 'short_summary', 'short_content', 'access_level', 'author', 'ip', 'has_enroll', 'has_fee', 'has_comment',
        'has_location', 'short_cover', 'short_photos', 'short_video', 'short_files', 'price', 'is_original', 'link', 'create_time',
        'update_time', 'short_logs', 'short_more', 'sort', 'language_code',
    )
    search_fields = (
        'title', 'subtitle', 'summary', 'content',
    )
    fields = (
        'id', 'is_deleted', 'category_id', 'classify_id', 'show', 'user_id', 'with_user_id', 'title',
        'subtitle', 'summary', 'content', 'access_level', 'author', 'ip', 'has_enroll', 'has_fee', 'has_comment',
        'has_location', 'cover', 'photos', 'video', 'files', 'price', 'is_original', 'link', 'create_time',
        'update_time', 'logs', 'more', 'sort', 'language_code',
    )
    readonly_fields = ('id', 'update_time',)  # 只读
    list_per_page = 10  # 每页显示10条
    ordering = ['-update_time']  # 排序

    # class Media:
    #     css = {
    #         'all': (
    #             '/css/fancy.css',
    #         )
    #     }

@admin.register(ThreadCategory)
class ThreadCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'platform_code', 'value', 'name', 'need_auth', 'short_description', 'sort', 'parent_id', "is_deleted")
    search_fields = ('id', 'platform_code', 'value', 'name',)
    fields = ('id', 'platform_code', 'value', 'name', 'need_auth', 'description', 'sort', 'parent_id', "is_deleted")
    readonly_fields = ('id',)
    ordering = ['platform_code', 'parent_id', 'sort']

@admin.register(ThreadClassify)
class ThreadClassifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'name', 'show', 'category', 'description', 'icon', 'sort', 'parent_id', "config")
    search_fields = ('id', 'value', 'name', 'show', 'category')
    fields = ('id', 'value', 'name', 'show', 'category', 'description', 'icon', 'sort', 'parent_id', "config")
    readonly_fields = ['id']
    ordering = ['category', 'parent_id', 'sort']

@admin.register(ThreadShow)
class ThreadShowAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'name', 'config', 'description')
    search_fields = ('id', 'value', 'name', 'config')
    fields = ('id', 'value', 'config', 'name', 'description')
    readonly_fields = ('id',)

@admin.register(ThreadExtendData)
class ThreadExtendDataAdmin(admin.ModelAdmin):
    list_display = (
        'thread_id', 'short_field_1', 'short_field_2', 'short_field_3', 'short_field_4', 'short_field_5',
        'short_field_6',
        'short_field_7',
        'short_field_8', 'short_field_9', 'short_field_10', 'short_field_11', 'short_field_12', 'short_field_13',
        'short_field_14',
        'short_field_15', 'short_field_16', 'short_field_17', 'short_field_18', 'short_field_19', 'short_field_20')
    search_fields = (
        'thread_id', 'short_field_1', 'short_field_2', 'short_field_3', 'short_field_4', 'short_field_5',
        'short_field_6',
        'short_field_7',
        'short_field_8', 'short_field_9', 'short_field_10', 'short_field_11', 'short_field_12', 'short_field_13',
        'short_field_14',
        'short_field_15', 'short_field_16', 'short_field_17', 'short_field_18', 'short_field_19', 'short_field_20')
    fields = ('thread_id', 'field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6', 'field_7',
              'field_8', 'field_9', 'field_10', 'field_11', 'field_12', 'field_13', 'field_14',
              'field_15', 'field_16', 'field_17', 'field_18', 'field_19', 'field_20')


@admin.register(ThreadExtendField)
class ThreadExtendFieldAdmin(admin.ModelAdmin):
    list_display = ("id", "category", 'field', 'field_index', 'value', 'type', 'unit')
    search_fields = ("category__value", 'field_index', 'type')
    fields = ('id', "category", 'field', 'field_index', 'value', 'type', 'unit', 'config')
    readonly_fields = ('id',)
    ordering = ['-category_id']
    list_per_page = 20  # 每页显示20条


@admin.register(ThreadTag)
class ThreadTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
    search_fields = ('id', 'value')
    fields = ('id', 'value',)
    readonly_fields = ('id',)


@admin.register(ThreadTagMapping)
class ThreadTagMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread_id', 'tag_id')
    search_fields = ('id', 'thread_id', 'tag_id')
    fields = ('thread_id', 'tag_id')


@admin.register(ThreadImageAuth)
class ThreadImageAuthAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
    search_fields = ('id', 'value')
    fields = ('id', 'value',)
    readonly_fields = ('id',)


# @admin.register(ThreadResource)
# class ThreadImageAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'name', 'url', 'filename', 'filetype', 'image_auth_id', 'price', 'snapshot', 'format', 'logs', 'user_id')
#     search_fields = (
#         'id', 'name', 'url', 'filename', 'filetype', 'image_auth_id', 'price', 'snapshot', 'format', 'logs', 'user_id')
#     fields = (
#         'id', 'name', 'url', 'filename', 'filetype', 'image_auth_id', 'price', 'snapshot', 'format', 'logs', 'user_id')
#     readonly_fields = ('id',)


@admin.register(ThreadStatistic)
class ThreadStatisticAdmin(admin.ModelAdmin):
    list_display = (
        'thread_id', 'flag_classifies', 'flag_weights', 'weight', 'views', 'plays', 'comments', 'likes',
        'favorite', 'shares',
    )
    search_fields = (
        'thread_id', 'flag_classifies', 'flag_weights', 'weight', 'views', 'plays', 'comments', 'likes',
        'favorite', 'shares',
    )
    fields = (
        'thread_id', 'flag_classifies', 'flag_weights', 'weight', 'views', 'plays', 'comments', 'likes',
        'favorite', 'shares',
    )


admin.site.site_header = config.get('main', 'app_name', 'msa一体化管理后台')
admin.site.site_title = config.get('main', 'app_name', 'msa一体化管理后台')
