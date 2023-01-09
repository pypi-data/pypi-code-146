from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from kfsdutils.apps.models.constants import MAX_LENGTH, MIN_LENGTH, IDENTIFIER_REGEX_CONDITION


class BaseModelManager(models.Manager):
    def get_by_natural_key(self, identifier):
        return self.get(identifier=identifier)


class BaseModel(models.Model):
    class Meta:
        abstract = True
        
    identifier = models.CharField(
        unique=True,
        max_length=MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=IDENTIFIER_REGEX_CONDITION,
                message="identifier doesnt match condition {}".format(IDENTIFIER_REGEX_CONDITION)
            ),
            MaxLengthValidator(MAX_LENGTH),
            MinLengthValidator(MIN_LENGTH)
        ]
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = BaseModelManager()

    def natural_key(self):
        return (self.identifier,)

    def __str__(self):
        return self.identifier
