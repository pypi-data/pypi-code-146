from django.contrib import admin, messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import re_path
from django.utils.translation import gettext_lazy as _

from .models import Broadcast


@admin.register(Broadcast)
class BroadcastModelAdmin(admin.ModelAdmin):
    menu_order = 9
    model = Broadcast
    menu_label = _("Broadcasts")
    list_display = ["title", "message", "sent_counter", "last_sent_at"]
    list_filter = ["last_sent_at"]

    def send_view(self, request, instance_pk):
        perm_name = self.permission_helper.get_perm_codename("send")
        obj = get_object_or_404(self.model, id=instance_pk)
        if not request.user.has_perm(perm_name):
            messages.add_message(
                request,
                level=messages.ERROR,
                message=_("You don't have any permissions to send notifications"),
            )
        else:
            obj.send(request.user)
            messages.add_message(
                request,
                level=messages.ERROR,
                message=_("Notification #{} sent.").format(obj.id),
            )
        return HttpResponseRedirect(self.url_helper.get_action_url("index"))

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls = urls + (
            re_path(
                self.url_helper.get_action_url_pattern("send"),
                self.send_view,
                name=self.url_helper.get_action_url_name("send"),
            ),
        )
        return urls
