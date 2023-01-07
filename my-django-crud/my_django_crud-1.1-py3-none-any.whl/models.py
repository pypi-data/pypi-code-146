from django.db import models

# Create your models here.


class Test(models.Model):
    item = models.CharField(max_length=100, default="")
    