from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.db.utils import OperationalError
from django.dispatch import receiver
from prj_drone_drf.drone_app.models.load_information import LoadInformation
from prj_drone_drf.drone_app.utils import validate_fleet_size


class Drone(models.Model):
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        help_text="Serial number of the drone"
    )

    DRONE_MODEL_CHOICES = [
        ('Lightweight', 'Lightweight'),
        ('Middleweight', 'Middleweight'),
        ('Cruiserweight', 'Cruiserweight'),
        ('Heavyweight', 'Heavyweight'),
    ]
    model = models.CharField(
        max_length=13,
        choices=DRONE_MODEL_CHOICES,
        default='Lightweight',
        help_text="Model of the drone"
    )

    weight_limit = models.DecimalField(
        validators=[
            MaxValueValidator(500),
            MinValueValidator(1)
        ],
        max_digits=5,
        decimal_places=2,
        help_text="Weight limit possible to carry. The max value is 500 grams."
    )

    battery_capacity = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],
        default=100,
        help_text="Current percent of battery's capacity. From 0% to 100%."
    )

    DRONE_STATE_CHOICES = [
        ('IDLE', 'IDLE'),
        ('LOADING', 'LOADING'),
        ('LOADED', 'LOADED'),
        ('DELIVERING', 'DELIVERING'),
        ('DELIVERED', 'DELIVERED'),
        ('RETURNING', 'RETURNING'),
    ]
    state = models.CharField(
        max_length=10,
        choices=DRONE_STATE_CHOICES,
        default='IDLE',
        help_text="State of the drone"
    )

    @property
    def load_info(self):
        return LoadInformation.objects.filter(drone__pk=self.pk)

    def __str__(self):
        return f'{self.serial_number}/{self.model} - cap: {self.weight_limit}'


@receiver(pre_save, sender=Drone)
def drone_validator(sender, instance, *args, **kwargs):
    validate_fleet_size(Drone, OperationalError)
