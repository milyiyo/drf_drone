# Generated by Django 4.0.4 on 2022-05-09 20:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drone_app', '0006_alter_drone_model_alter_drone_state_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='weight',
            field=models.DecimalField(decimal_places=2, help_text='Weight of the medication in grams', max_digits=5, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
