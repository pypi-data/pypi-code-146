from django.contrib import admin
from .models import AuthRequest, AuthFailure


@admin.register(AuthRequest)
class AuthRequestAdmin(admin.ModelAdmin):
    list_display = ("email", "type", "email_sent", "is_used", "created")
    list_filter = ("type", "email_sent", "is_used")
    readonly_fields = (
        "email",
        "type",
        "hash",
        "otp",
        "email_sent",
        "is_used",
        "user",
        "created",
    )


@admin.register(AuthFailure)
class AuthFailureAdmin(admin.ModelAdmin):
    list_display = ("created",)
    readonly_fields = ("hash",)
