from django.contrib.auth.models import User
import json
from django.db import models
from pyzstd import decompress, compress


class TextChoices(models.TextChoices):
    @classmethod
    def list_codes(cls):
        return [code for code, label in cls.choices]


class AbstractCreatedUpdatedModel(models.Model):
    created_at = models.DateTimeField("crée le", auto_now_add=True)
    updated_at = models.DateTimeField("maj le", auto_now=True)

    class Meta:
        abstract = True


class AbstractSsoUser(AbstractCreatedUpdatedModel, models.Model):
    sso_uuid = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    list_apps = models.JSONField()
    user = models.OneToOneField(User, related_name="sso_user", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Reference(AbstractCreatedUpdatedModel):
    code = models.CharField(max_length=20, primary_key=True)
    label = models.CharField(max_length=100)

    class Meta:
        abstract = True
        ordering = ["label"]

    def __str__(self):
        return self.label


class CompressedJsonField(models.BinaryField):
    description = "Compress field - specially used for logs fields"

    def get_db_prep_value(self, value, connection, prepared=False):
        return compress(json.dumps(value).encode("utf-8"))

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        value = decompress(bytes(value)).decode("utf8")
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value


class CompressedTextField(models.BinaryField):
    description = "Compress Text field"

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is not None:
            return compress(value.encode("utf-8"))
        return value

    def to_python(self, value):
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            return decompress(bytes(value)).decode("utf-8")
        return value
