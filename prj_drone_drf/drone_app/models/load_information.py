from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _


class LoadInformation(models.Model):
    drone = models.ForeignKey('Drone', on_delete=CASCADE)
    medication = models.ForeignKey('Medication', on_delete=CASCADE)
    quantity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
        ],
        help_text='Amount of medications that is loaded')

    def __str__(self) -> str:
        return f"Drone: {self.drone.pk}, Med: {self.medication.pk}, Quantity: {self.quantity}"
