from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse

from huscy.consents.models import Consent, ConsentFile
from huscy.project_consents.models import ProjectConsent, ProjectConsentFile
from huscy.consents.views import CreateConsentView, SignConsentView
from huscy.projects.models import Project
from huscy.subjects.models import Subject


class CreateProjectConsentView(CreateConsentView):

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        response = super().post(self, request, *args, **kwargs)
        consent = Consent.objects.latest('id')
        ProjectConsent.objects.create(consent=consent, project=self.project)
        return response

    def get_success_url(self):
        return reverse('consent-created')


class CreateProjectConsentFileView(SignConsentView):

    def dispatch(self, request, *args, **kwargs):
        self.project_consent = get_object_or_404(
            ProjectConsent,
            project_id=self.kwargs['project_id']
        )
        self.subject = get_object_or_404(Subject, pk=self.kwargs['subject_id'])
        self.consent = self.project_consent.consent  # required by parent class
        return super(SignConsentView, self).dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        response = super().post(self, request, *args, **kwargs)
        consent_file = ConsentFile.objects.latest('id')
        ProjectConsentFile.objects.create(
            consent_file=consent_file,
            project_consent=self.project_consent,
            subject=self.subject
        )
        return response
