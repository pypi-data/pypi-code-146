from django.db import models

from huscy.consents.models import Consent, ConsentFile
from huscy.projects.models import Project
from huscy.subjects.models import Subject


class ProjectConsentCategory(models.Model):
    name = models.CharField(max_length=255)
    text_fragments = models.JSONField(default=[])


class ProjectConsent(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    consent = models.ForeignKey(Consent, on_delete=models.PROTECT)


class ProjectConsentFile(models.Model):
    project_consent = models.ForeignKey(ProjectConsent, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    consent_file = models.OneToOneField(ConsentFile, on_delete=models.PROTECT)

    class Meta:
        unique_together = 'project_consent', 'subject'
