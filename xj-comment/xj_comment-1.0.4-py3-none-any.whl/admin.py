from django.contrib import admin
from .models import *


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_deleted', 'thread_id', 'user_id', 'ip', 'message', 'commented_id',
                    'weight', 'likes', 'favorite', 'comments', 'shares')
    search_fields = ('id', 'is_deleted', 'thread_id', 'user_id', 'ip', 'message', 'commented_id',
                     'weight', 'likes', 'favorite', 'comments', 'shares')
    fields = ('is_deleted', 'thread_id', 'user_id', 'ip', 'message', 'commented_id',
              'weight', 'likes', 'favorite', 'comments', 'shares')


# Register your models here.
admin.site.register(Comment, CommentAdmin)
admin.site.register(Comment1, CommentAdmin)
admin.site.register(Comment2, CommentAdmin)
admin.site.register(Comment3, CommentAdmin)
admin.site.register(Comment4, CommentAdmin)
admin.site.register(Comment5, CommentAdmin)
admin.site.register(Comment6, CommentAdmin)
admin.site.register(Comment7, CommentAdmin)
admin.site.register(Comment8, CommentAdmin)
admin.site.register(Comment9, CommentAdmin)
