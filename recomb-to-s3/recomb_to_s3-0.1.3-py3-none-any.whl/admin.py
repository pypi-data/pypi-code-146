from django.contrib import admin

from recomb_to_s3.models import RecombToS3


@admin.register(RecombToS3)
class RecombToS3Admin(admin.ModelAdmin):
    list_display = ("id", "author", "file", "created_at")
    list_filter = ("author", "created_at", "file_type")
