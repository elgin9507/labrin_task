from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
import json

from .models import Todo, Comment


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.task_group_name = 'task_{}'.format(self.task_id)
        self.user = self.scope['user']
        task = Todo.objects.get(pk=self.task_id)
        self.task = task
        if self.user.username:
            await self.channel_layer.group_add(
                self.task_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            raise DenyConnection('Unauthorized')

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.task_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        todo_obj = Todo.objects.get(pk=self.task_id)
        print("AAAAAAAAAAAAAAAAAAAa")
        print(text_data_json)
        text = text_data_json['message']
        comment_obj = Comment.objects.create(todo=todo_obj,
                                             author=self.user,
                                             text=text)
        response_data = {
            'pk': comment_obj.id,
            'user_name': comment_obj.author.username,
            'text': comment_obj.text,
            'date': comment_obj.created_at.strftime("%b %d %H:%M %p")
        }

        await self.channel_layer.group_send(
            self.task_group_name,
            {
                'type': 'comment_message',
                'message': response_data
            }
        )

    async def comment_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
