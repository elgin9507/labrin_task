from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.TodoListView.as_view(), name='index'),
    url(r'^create-task/$', views.TodoCreateView.as_view(), name='create-todo'),
    url(r'^todos/(?P<pk>[0-9]+)/$', views.TodoDetailView.as_view(), name='todo-detail'),
    url(r'^todo/(?P<pk>[0-9]+)/delete/$', views.TodoDeleteView.as_view(), name='todo-delete'),
    url(r'^add-comment/$', views.CommentCreateView.as_view(), name='add-comment'),
    url(r'^share-task/$', views.ShareTodoView.as_view(), name='todo-share')
]
