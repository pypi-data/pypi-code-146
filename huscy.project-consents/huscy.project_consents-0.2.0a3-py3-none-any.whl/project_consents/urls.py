from django.urls import path
from huscy.project_consents import views

urlpatterns = [
    path(
        '<int:project_id>/consents/',
        views.CreateProjectConsentView.as_view(),
        name="create-project-consent"
    ),
    path(
        '<int:project_id>/subjects/<uuid:subject_id>/consents/',
        views.CreateProjectConsentFileView.as_view(),
        name="sign-project-consent"),
]
