from django.urls import path

from . import views

schema_urls = [
    path("", views.create_db_schema_graph_model_view, name="db_schema"),
]
