from dnoticias_backoffice import views

from django.urls import path


urlpatterns = [
    path("flagstate/", views.FlagStateListView.as_view(), name="flag-state-list-view"),
    path("flagstate/create/", views.FlagStateCreateView.as_view(), name="flag-state-create-view"),
    path("flagstate/<int:pk>/", views.FlagStateEditView.as_view(), name="flag-state-wildcard-view"),
    path("flagstate/delete/<int:pk>/", views.FlagStateDeleteView.as_view(), name="flag-state-delete-view"),

    path("group/", views.GroupListView.as_view(), name="group-list-view"),
    path("group/create/", views.GroupCreateView.as_view(), name="group-create-view"),
    path("group/<int:pk>/", views.GroupEditView.as_view(), name="group-detail-view"),
    path("group/delete/<int:pk>/", views.GroupDeleteView.as_view(), name="group-delete-view"),

    path("permissions/", views.PermissionsView.as_view(), name="permissions"),
    path("permissions/user/", views.UserPermissionsView.as_view(), name="permissions-per-user"),
    path("permissions/group/", views.GroupPermissionsView.as_view(), name="permissions-per-group"),
    path("groups/user/", views.UserGroupsView.as_view(), name="groups-per-user"),
    
    path('select2/users/', views.UsersSelect2View.as_view(), name="users-select2"),
    path('select2/permissions/', views.PermissionsSelect2View.as_view(), name="permissions-select2"),
]
