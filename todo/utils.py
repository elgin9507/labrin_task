from django.contrib.auth import get_user_model
import datetime

UserModel = get_user_model()


def get_user_by_email_or_username(value):
    user_by_name = UserModel.objects.filter(username=value)
    user_by_email = UserModel.objects.filter(email=value)
    if user_by_name.exists():
        return user_by_name.last()
    elif user_by_email.exists():
        return user_by_email.last()
    else:
        return None


def get_secs_until_10_minutes_before(date_time):
    """
    Function for getting datetime of task deadline reminder email (10 minutes
    before). Result is passed to celery task, which asynchronously run this
    function.
    """
    deadline_remind_time = date_time - datetime.timedelta(minutes=10)
    secs_until_reminder = (deadline_remind_time - datetime.datetime.now()).total_seconds()
    if secs_until_reminder < 0:
        return 0
    return secs_until_reminder
