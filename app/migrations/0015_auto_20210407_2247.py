# Generated by Django 3.1.7 on 2021-04-07 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20210407_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='is_accepted',
            field=models.BooleanField(default=False, verbose_name='Подтвержден'),
        ),
        migrations.DeleteModel(
            name='MasterRequest',
        ),
    ]
