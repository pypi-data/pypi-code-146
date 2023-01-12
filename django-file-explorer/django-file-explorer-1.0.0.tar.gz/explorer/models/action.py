from django.db import models
from django.utils import timezone


class ActionManager(models.Manager):
    def __init__(self) -> None:
        super().__init__()
    
    def getIfExists(self, option_name):
        queryset = self.filter(name=option_name)
        if queryset.exists():
            return queryset.first()
        return None

class Action(models.Model):
    name = models.CharField(max_length=120)
    creation_date = models.DateTimeField(default=timezone.now)

    actions = ActionManager()

    def __str__(self) -> str:
        return self.name

    # GETTERS
    def getName(self):
        """Get the name of option."""
        return self.name