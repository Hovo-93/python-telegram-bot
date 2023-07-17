"""
Файл настроек Celery
https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
"""
from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
import django

# этот код скопирован с manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_bot.settings')
django.setup()

# здесь вы меняете имя
app = Celery("telegram_bot")

# Для получения настроек Django, связываем префикс "CELERY" с настройкой celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# загрузка tasks.py в приложение django
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-google_sheets_table': {
        'task': 'python_telegram_bot.tasks.run_management_command',
        'schedule': crontab(minute='*/1')
    },

}