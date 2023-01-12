from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from .action import Action
from .volume import Volume

class UserRoleManager(models.Manager):
    def __init__(self) -> None:
        super().__init__()
    
    def getIfExists(self, **kwargs):
        queryset = self.filter(**kwargs)
        if queryset.exists():
            return queryset.first()
        return None

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE)
    actions = models.ManyToManyField(Action, blank=True)
    creation_date = models.DateTimeField(default=timezone.now)

    userroles = UserRoleManager()

    def __str__(self) -> str:
        return self.user.username

    # GETTERS
    def getUser(self):
        """Get the user."""
        return self.user

    def getVolume(self):
        """Return the volum."""
        return self.volume

    def getActions(self):
        """Return the operations."""
        return self.actions