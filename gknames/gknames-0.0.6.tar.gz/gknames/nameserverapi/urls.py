from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'eventsapi', views.EventsViewSet)

# For my generic serializer, I had to set basename to something.
#router.register(r'eventapi', views.EventView, basename = "event")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('eventapi/', views.EventView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
