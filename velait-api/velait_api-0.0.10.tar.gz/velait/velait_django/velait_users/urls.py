from velait.velait_django.velait_users.views import user_logout_view, user_login_view, user_authentication_view
from django.urls import path

app_name = "apps.velait_users"

urlpatterns = [
    path("logout/", user_logout_view, name="logout"),
    path("login/", user_login_view, name="login"),
    path('authenticate/', user_authentication_view, name="authenticate"),
]
