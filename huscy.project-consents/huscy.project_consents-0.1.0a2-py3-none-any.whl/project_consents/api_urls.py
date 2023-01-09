from rest_framework.routers import DefaultRouter

from .viewsets import ProjectConsentCategoryViewSet


router = DefaultRouter()
router.register('projectconsentcategories', ProjectConsentCategoryViewSet,
                basename='projectconsentcategory')


urlpatterns = router.urls
