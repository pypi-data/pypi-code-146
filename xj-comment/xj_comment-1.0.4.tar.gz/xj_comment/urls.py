from django.conf.urls import url
from .apis import CommentListView, CommentDetailView

urlpatterns = [
    url(r'^list/?$', CommentListView.as_view(), name='lists'),
    url(r'^list/(?P<pk>\d+)/?$', CommentDetailView.as_view(), name='detail'),
]
