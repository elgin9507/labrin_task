from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail


@shared_task()
def send_todo_reminder(user_email, task_name):
    send_mail(
        '10 minutes left to the deadline of {}'.format(task_name),
        'Dear user, please be reminded that task "{}" '
        'has only 10 minutes left to be completed'.format(task_name),
        'labrin@site.com',
        [user_email],
    )
