from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
#from NewsPaper import settings
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .tasks import send_notifications_by_task

from news.models import PostCategory


def send_notifications(title, preview, pk, email_list):
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


# отправка писем при публикации новой статьи
@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()
        subcribers: list[str] = []
        for cat in categories:
            subcribers += cat.subscribers.all()
        emails_list = [s.email for s in subcribers]

        #send_notifications(instance.title, instance.preview(), instance.pk, emails_list) # закоментим, чтобы отправлять через celery
        # рассылка через celery
        print(f'call function({send_notifications_by_task})')
        print(f'instance.title is {type(instance.title)}')
        print(f'instance.preview is {type(instance.preview)}')
        print(f'instance.pk is {type(instance.pk)}')
        print(f'emails_list is {type(emails_list)}')
        send_notifications_by_task.delay(instance.title,
                                                       instance.preview(), instance.pk, emails_list)