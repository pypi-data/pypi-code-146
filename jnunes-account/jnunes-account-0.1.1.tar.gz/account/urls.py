from django.contrib.auth import views as django_views
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetDoneView
from django.urls import path

from account import views
from account.views import CustomLoginView, CustomPasswordChangeView, CustomPasswordResetView
from account.views import CustomPasswordResetConfirmView

app_name = 'account'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logedout/', django_views.LogoutView.as_view(), name='logout'),
    path('change_password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='reset_password_complete'),
    path('signup/', views.signup_view, name='signup'),
    path('dummy/', views.dummy_view, name='dummy'),

]
