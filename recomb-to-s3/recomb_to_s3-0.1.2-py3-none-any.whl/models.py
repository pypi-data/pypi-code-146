from django.contrib.auth import get_user_model
from django.db import models

from recomb_to_s3.utils import directory_path

User = get_user_model()


class AbstractRecombToS3(models.Model):
    """abstract class with basic fields to record a file upload to s3."""

    file = models.FileField(upload_to=directory_path, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return self.file.name

    class Meta:
        abstract = True
        verbose_name = "uploaded file"
        ordering = ("-created_at",)


class RecombToS3(AbstractRecombToS3):
    """implement the abstract class"""

    class Meta(AbstractRecombToS3.Meta):
        abstract = False
