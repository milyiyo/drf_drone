
from celery.app import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def check_drones_battery():
    from prj_drone_drf.drone_app.models.drone import Drone
    fleet = Drone.objects.all()
    for drone in fleet:
        logger.info(
            f'id: {drone.pk}, serial_number: {drone.serial_number}, battery_capacity: {drone.battery_capacity}')
