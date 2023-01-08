from django.urls import path
from .api import (
    PartyTypeListCreateApi,
    SignListListCreateApi,
    TransitionApiView ,
    ActionListApi,
    DetailsListApiView,
    FlowModelGetApi,
    WorkFlowitemsListApi,
    WorkEventsListApi,
    statesListCreateApi,
    TransitionResetApiview
)

# updated
urlpatterns = [
    path('action/',ActionListApi.as_view()),
    path('model/',DetailsListApiView.as_view()),
    path('flowmodel/',FlowModelGetApi.as_view()),
    path('workflowitems/<int:pk>/',WorkFlowitemsListApi.as_view()),
    path('workevents/<int:pk>/',WorkEventsListApi.as_view()),
    path('transition/',TransitionApiView.as_view()),
    path('transition/reset/',TransitionResetApiview.as_view()),
    path('states/',statesListCreateApi.as_view()),
    path('party-type/',PartyTypeListCreateApi.as_view()),
    path('signatures/',SignListListCreateApi.as_view()),
]
