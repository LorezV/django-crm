# Generated by Django 3.1.7 on 2021-04-07 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210405_2333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='telegram',
        ),
    ]