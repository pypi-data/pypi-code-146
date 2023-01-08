from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Reason(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Activity(models.Model):
    topics = models.ManyToManyField(Topic)
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE, blank=True, null=True)
