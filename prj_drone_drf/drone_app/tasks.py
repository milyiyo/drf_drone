from celery.app import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def add_numbers(a, b):
    print(['test_task', a, b])
