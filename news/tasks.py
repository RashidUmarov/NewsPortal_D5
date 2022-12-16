from celery import shared_task, Celery
import time
from django.template.loader import render_to_string
from NewsPaper import settings
from django.core.mail import EmailMultiAlternatives
import datetime
from news.models import Post, Category
app = Celery('news')

# рассылка писем
@shared_task
def send_notifications_by_task(title, preview, pk, email_list):
    html_content = render_to_string(
        'new_post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=email_list,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

# рассылка писем о новых статьях/постах за неделю
#@shared_task - это не работает в Windows
@app.task
def notify_subscribers_about_weekly_news(): # это копия функции my_job() из runapscheduler.py
    today = datetime.datetime.now()
    week_ago = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(created__gte=week_ago)
    categories = set(posts.values_list('categories__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list("subscribers__email", flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    print(f'subcribers_email_list={subscribers}')
    print(f' send weekly notifications about new posts fro week from notify_subscribers_about_weekly_news()')
    msg = EmailMultiAlternatives(
        subject="Статьи за неделю",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)

