from __future__ import absolute_import

import os

from celery import Celery
from celery.utils.log import get_task_logger
from prj_drone_drf.drone_app.tasks import check_drones_battery

logger = get_task_logger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prj_drone_drf.settings')

app = Celery('prj_drone_drf')
app.config_from_object('django.conf:settings', namespace='CELERY')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        10.0, check_drones_battery.s(), name='[check_drones_battery] every 10')
