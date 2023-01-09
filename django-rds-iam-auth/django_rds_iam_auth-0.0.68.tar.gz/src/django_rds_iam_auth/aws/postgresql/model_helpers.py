from django.conf import settings
from django.db import models


class AbstractModel:
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(settings.TENANT_MODEL, on_delete=models.PROTECT)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AbstractModelNoId():
    tenant = models.ForeignKey(settings.TENANT_MODEL, on_delete=models.PROTECT)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AbstractModelBasic():
    tenant = models.ForeignKey(settings.TENANT_MODEL, on_delete=models.PROTECT)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)