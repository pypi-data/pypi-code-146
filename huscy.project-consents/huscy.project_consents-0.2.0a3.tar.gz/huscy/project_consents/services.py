from .models import ProjectConsent
from huscy.consents.services import create_consent, update_consent


def create_project_consent(project, name, text_fragments):
    consent = create_consent(name, text_fragments)
    return ProjectConsent.objects.create(project=project, consent=consent)


def update_project_consent(project_consent, name=None, text_fragments=None):
    update_consent(project_consent.consent, name, text_fragments)
    return project_consent
