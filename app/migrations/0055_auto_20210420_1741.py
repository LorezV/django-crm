# Generated by Django 3.1.7 on 2021-04-20 12:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_auto_20210420_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='working_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 20, 13, 41, 37, 361266, tzinfo=utc), verbose_name='Когда начинать работу'),
        ),
        migrations.AlterField(
            model_name='spending',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата расхода'),
        ),
    ]