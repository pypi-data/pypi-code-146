from django.db import models
from django.utils import timezone


class VolumeManager(models.Manager):
    def __init__(self) -> None:
        super().__init__()
    
    def getIfExists(self, volume_name):
        queryset = self.filter(name=volume_name)
        if queryset.exists():
            return queryset.first()
        return None

class Volume(models.Model):
    name = models.CharField(max_length=120)
    path = models.CharField(max_length=2048)
    active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(default=timezone.now)

    volumes = VolumeManager()

    def __str__(self) -> str:
        return self.name

    # GETTERS
    def getName(self):
        """Get the name of volume"""
        return self.name

    def getPath(self):
        """Return the volume path."""
        return self.path

    def isActive(self):
        """Return the active status of volume."""
        return self.active