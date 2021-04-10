# Generated by Django 3.1.7 on 2021-04-05 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210405_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=128, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=128, verbose_name='Фамилия')),
                ('telegram', models.CharField(blank=True, max_length=128, verbose_name='Телеграм')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='telegram',
            field=models.CharField(blank=True, max_length=128, verbose_name='Телеграм'),
        ),
        migrations.AlterField(
            model_name='order',
            name='master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.master'),
        ),
    ]
