from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Todo(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)


class ShareTodo(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    with_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment_allowed = models.BooleanField(default=False)
