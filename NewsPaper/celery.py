import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_email_about_new_posts_every_monday': {
        'task': 'news.tasks.notify_subscribers_about_weekly_news',
        'schedule': crontab(hour=03, minute=00, day_of_week=1),
    },
}

app.autodiscover_tasks()
