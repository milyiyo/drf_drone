from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class Medication(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        validators=[RegexValidator(
            r"^[a-zA-Z0-9-_]+$", "Allowed only letters, numbers, ‘-‘, ‘_’.")],
        help_text="Name of the medication"
    )

    weight = models.DecimalField(
        validators=[
            MinValueValidator(1)
        ],
        max_digits=5,
        decimal_places=2,
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
        null=True,
        help_text="Image of the medication"
    )

    def __str__(self):
        return f'{self.name}/{self.code} - cap: {self.weight}'
