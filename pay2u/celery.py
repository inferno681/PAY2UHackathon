# flake8: noqa
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pay2u.settings')

app = Celery('pay2u')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
