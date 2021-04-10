# Generated by Django 3.1.7 on 2021-04-05 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='client_city',
            field=models.CharField(max_length=128, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(choices=[('G', 'Гарантия'), ('N', 'Обычный')], default='N', max_length=1, verbose_name='Тип'),
        ),
    ]
