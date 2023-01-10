from django.views.generic import TemplateView
from django.urls import path

from huscy.consents import views

urlpatterns = [
    path('<int:consent_id>/', views.SignConsentView.as_view(), name='sign-consent'),
    path('create/', views.CreateConsentView.as_view(), name='create-consent'),
    path(
        'create/success/',
        TemplateView.as_view(template_name='consents/success.html'),
        name='consent-created'
    ),
]
