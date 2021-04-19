# Generated by Django 3.1.7 on 2021-04-18 19:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_auto_20210419_0035'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='clear_amount_calculated',
            new_name='clear_amount',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='master_amount_calculated',
            new_name='master_amount',
        ),
        migrations.AlterField(
            model_name='order',
            name='working_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 18, 20, 45, 4, 149830, tzinfo=utc), verbose_name='Когда начинать работу'),
        ),
    ]
