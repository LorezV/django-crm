# Generated by Django 3.1.7 on 2021-04-10 19:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20210410_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='working_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 10, 20, 13, 34, 713050, tzinfo=utc), verbose_name='Когда начинать работу'),
        ),
    ]
