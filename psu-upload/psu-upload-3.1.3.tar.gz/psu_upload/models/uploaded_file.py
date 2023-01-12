from django.db import models
from psu_base.classes.Log import Log
import math
import os

log = Log()


class UploadedFile(models.Model):
    """File Uploaded to S3 via psu-upload"""

    # Fields
    app_code = models.CharField(
        max_length=15,
        verbose_name="Application Code",
        help_text="Application that this file belongs to.",
        db_index=True,
        blank=False,
        null=False,
    )
    owner = models.CharField(
        max_length=128,
        help_text="This holds username of the user that uploaded the file, which could be a provisional email address",
        blank=True,
        null=True,
    )
    content_type = models.CharField(max_length=128, blank=False, null=False)
    size = models.IntegerField(blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    # Although this can be obtained from the file object, having path and basename in the
    # database allows easier searching of the files via DB query
    s3_path = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        help_text="Full S3 file path",
    )
    basename = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        db_index=True,
        help_text="File name without the path info",
    )
    original_name = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        help_text="Name of file as uploaded by user",
    )
    tag = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text="Any sort of tag that will be useful for looking up files",
    )
    foreign_table = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default=None,
        db_index=True,
        help_text="table or model that this file belongs to",
    )
    foreign_key = models.IntegerField(
        blank=True,
        null=True,
        default=None,
        db_index=True,
        help_text="ID of a record in another table that this file belongs to",
    )
    status = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        db_index=True,
        help_text="Allow flags for Deleted, Archived, or maybe someday Scanned (for viruses)",
    )

    def readable_size(self):
        if self.size == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(self.size, 1024)))
        p = math.pow(1024, i)
        s = round(self.size / p, 1)
        return "%s %s" % (s, size_name[i])

    def is_image(self):
        return "image" in self.content_type

    def is_code(self):
        for x in ["html", "css", "javascript", "php", "csh", "java", "x-sh"]:
            if x in self.content_type:
                return True
        return False

    def icon_class(self):
        if self.is_image():
            return "fa fa-file-image-o"
        if "pdf" in self.content_type:
            return "fa fa-file-pdf-o"
        if "audio" in self.content_type:
            return "fa fa-file-audio-o"
        if "video" in self.content_type:
            return "fa fa-file-video-o"
        if self.is_code():
            return "fa fa-file-code-o"
        if "zip" in self.content_type:
            return "fa fa-file-zip-o"
        if "word" in self.content_type:
            return "fa fa-file-word-o"
        if "excel" in self.content_type or "sheet" in self.content_type:
            return "fa fa-file-excel-o"
        if "powerpoint" in self.content_type or "presentation" in self.content_type:
            return "fa fa-file-powerpoint-o"

        # This must come last to eliminate code files being identifies as text
        if "text" in self.content_type and "calendar" not in self.content_type:
            return "fa fa-file-text-o"

        # All other types
        return "fa fa-file-o"
