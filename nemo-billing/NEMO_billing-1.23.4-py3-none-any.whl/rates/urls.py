from NEMO.urls import router
from django.urls import path

from NEMO_billing.rates import api, views

# Rest API URLs
router.register(r"rates", api.RateViewSet)
router.register(r"rate_types", api.RateTypeViewSet)

urlpatterns = [
    path("rates/", views.rates, name="rates"),
    path("rates/<str:rate_type_choice>/", views.rates, name="rates"),
    path("rate/", views.create_or_modify_rate, name="create_rate"),
    path("rate/<str:rate_type_choice>/", views.create_or_modify_rate, name="create_rate"),
    path("rate/<str:rate_type_choice>/<int:item_id>/", views.create_or_modify_rate, name="create_rate"),
    path("rate_form/", views.new_time_rate_form, name="new_time_rate_form"),
    path("rate_time/<int:rate_id>/", views.delete_rate_time, name="delete_rate_time"),
]
