from django.db import models

class PWASettings(models.Model):
  title = models.CharField(max_length=250)
  description = models.CharField(max_length=255)
  color = models.CharField(max_length=7, help_text="Color in hex. e.g #f08743")