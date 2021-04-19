# Generated by Django 3.1.7 on 2021-04-18 18:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_auto_20210418_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='clear_amount',
            field=models.IntegerField(blank=True, null=True, verbose_name='Чистая прибыль'),
        ),
        migrations.AddField(
            model_name='order',
            name='master_amount',
            field=models.IntegerField(blank=True, null=True, verbose_name='Сумма ВМ'),
        ),
        migrations.AlterField(
            model_name='order',
            name='working_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 18, 19, 27, 39, 493817, tzinfo=utc), verbose_name='Когда начинать работу'),
        ),
    ]
