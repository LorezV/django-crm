# Generated by Django 3.1.7 on 2021-04-19 08:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_auto_20210419_0045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='clear_amount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='master_amount',
        ),
        migrations.AlterField(
            model_name='order',
            name='working_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 19, 9, 45, 9, 88896, tzinfo=utc), verbose_name='Когда начинать работу'),
        ),
    ]
