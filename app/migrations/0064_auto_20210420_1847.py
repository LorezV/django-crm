# Generated by Django 3.1.7 on 2021-04-20 13:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0063_auto_20210420_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='working_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 20, 14, 47, 41, 895655, tzinfo=utc), verbose_name='Когда начинать работу'),
        ),
    ]
