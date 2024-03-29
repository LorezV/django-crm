# Generated by Django 3.1.7 on 2021-04-20 13:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0060_auto_20210420_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='working_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 20, 14, 46, 43, 427054, tzinfo=utc), verbose_name='Когда начинать работу'),
        ),
        migrations.AlterField(
            model_name='spending',
            name='spending_type',
            field=models.SmallIntegerField(choices=[(0, 'Реклама оплата труда'), (1, 'Реклама материал'), (2, 'Реклама интернет'), (3, 'Зарплата Руководителя'), (4, 'Зарплата Подчиненых'), (5, 'Командировка'), (6, 'Аренда'), (7, 'Инкасация'), (8, 'Перенос с прошлого мес.')], default=0, max_length=1, verbose_name='Тип'),
        ),
    ]
