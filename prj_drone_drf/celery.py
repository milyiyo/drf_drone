from __future__ import absolute_import

import os

from django.conf import settings

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from prj_drone_drf.drone_app.tasks import add_numbers

logger = get_task_logger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prj_drone_drf.settings')
app = Celery()

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, add_numbers.s(
        1, 2), name='[add_numbers] every 10')

    # # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )


@app.task
def test(arg):
    logger.info(['test_task', arg])
