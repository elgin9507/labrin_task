from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^comment/(?P<task_id>.*)/$', consumers.CommentConsumer),
]
