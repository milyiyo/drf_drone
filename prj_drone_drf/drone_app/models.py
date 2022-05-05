from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models


class Medication(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        validators=[RegexValidator(
            r"^[a-zA-Z0-9-_]+$", "Allowed only letters, numbers, ‘-‘, ‘_’.")],
        help_text="Name of the medication"
    )

    weight = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ],
        help_text="Weight of the medication in grams"
    )

    code = models.CharField(
        max_length=200,
        unique=True,
        validators=[RegexValidator(
            r"^[A-Z0-9_]+$", "Allowed only upper case letters, underscore and numbers.")],
        help_text="Code of the medication"
    )

    image = models.ImageField(
        upload_to="images_med",
        help_text="Image of the medication"
    )


class Drone(models.Model):
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        help_text="Serial number of the drone"
    )

    DRONE_MODEL_CHOICES = [
        ('LW', 'Lightweight'),
        ('MW', 'Middleweight'),
        ('CW', 'Cruiserweight'),
        ('HW', 'Heavyweight'),
    ]
    model = models.CharField(
        max_length=13,
        choices=DRONE_MODEL_CHOICES,
        default='LW',
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
        ('IE', 'IDLE'),
        ('LG', 'LOADING'),
        ('LD', 'LOADED'),
        ('DG', 'DELIVERING'),
        ('DD', 'DELIVERED'),
        ('RG', 'RETURNING'),
    ]
    state = models.CharField(
        max_length=10,
        choices=DRONE_STATE_CHOICES,
        default='IE',
        help_text="State of the drone"
    )

    medications = models.ManyToManyField(Medication, related_name="drones", blank=True)
