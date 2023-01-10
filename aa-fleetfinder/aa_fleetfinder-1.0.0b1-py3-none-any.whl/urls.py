"""
URL config
"""

# Django
from django.urls import include, path

# AA Fleet Finder
from fleetfinder import views

app_name: str = "fleetfinder"

urlpatterns = [
    path(route="", view=views.dashboard, name="dashboard"),
    path(route="create/", view=views.create_fleet, name="create_fleet"),
    path(route="save/", view=views.save_fleet, name="save_fleet"),
    path(route="join/<int:fleet_id>/", view=views.join_fleet, name="join_fleet"),
    path(
        route="details/<int:fleet_id>/", view=views.fleet_details, name="fleet_details"
    ),
    path(route="edit/<int:fleet_id>/", view=views.edit_fleet, name="edit_fleet"),
    # Ajax calls
    path(
        route="ajax/",
        view=include(
            [
                path(
                    route="dashboard/", view=views.ajax_dashboard, name="ajax_dashboard"
                ),
                path(
                    route="details/<int:fleet_id>/",
                    view=views.ajax_fleet_details,
                    name="ajax_fleet_details",
                ),
            ]
        ),
    ),
]
