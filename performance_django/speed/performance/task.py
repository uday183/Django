from celery.decorators import task
import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string



@task(name="create_users")
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return '{} random users created with success!'.format(total)


@task(name='summary') 
def summary():
    total=5
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return '{} random users created with success!'.format(total)

# to work django celerybeat run two instanse
# 1).celery -A speed worker -l info
# 2).celery -A speed beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler