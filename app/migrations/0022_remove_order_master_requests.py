# Generated by Django 3.1.7 on 2021-04-08 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20210408_2251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='master_requests',
        ),
    ]