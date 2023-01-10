from rest_framework.routers import DefaultRouter

from .viewsets import ConsentViewSet


router = DefaultRouter()
router.register('consents', ConsentViewSet, basename='consent')


urlpatterns = router.urls
