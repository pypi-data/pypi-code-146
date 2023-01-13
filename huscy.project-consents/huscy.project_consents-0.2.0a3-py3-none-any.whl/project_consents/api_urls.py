from rest_framework.routers import DefaultRouter

from .viewsets import ProjectConsentViewSet, ProjectConsentCategoryViewSet
from huscy.projects.api_urls import project_router


router = DefaultRouter()
router.register('projectconsentcategories', ProjectConsentCategoryViewSet,
                basename='projectconsentcategory')

project_router.register('consents', ProjectConsentViewSet, basename='projectconsent')


urlpatterns = router.urls
urlpatterns += project_router.urls
