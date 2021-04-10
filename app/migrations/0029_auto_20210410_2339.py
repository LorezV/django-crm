# Generated by Django 3.1.7 on 2021-04-10 18:39

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_auto_20210410_2327'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_first_name', models.CharField(blank=True, max_length=128, verbose_name='Имя')),
                ('telegram_last_name', models.CharField(blank=True, max_length=128, verbose_name='Фамилия')),
                ('telegram_username', models.CharField(blank=True, max_length=128, null=True, verbose_name='Telegram имя пользователя')),
                ('telegram_chat_id', models.CharField(max_length=128, verbose_name='Telegram id чата')),
                ('is_master', models.BooleanField(blank=True, default=False, verbose_name='Является мастером?')),
                ('is_operator', models.BooleanField(blank=True, default=False, verbose_name='Является оператором?')),
            ],
            options={
                'verbose_name': 'Мастер',
                'verbose_name_plural': 'Мастера',
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='working_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 10, 19, 39, 59, 283188, tzinfo=utc), verbose_name='Когда начинать работу'),
        ),
        migrations.AlterField(
            model_name='order',
            name='master',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_accepted': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', related_query_name='order', to='app.telegramprofile'),
        ),
        migrations.AlterField(
            model_name='order',
            name='master_requests',
            field=models.ManyToManyField(blank=True, limit_choices_to={'is_accepted': True}, related_name='orders_request', related_query_name='order_request', to='app.TelegramProfile', verbose_name='Предложения мастерам'),
        ),
        migrations.DeleteModel(
            name='TelegramMaster',
        ),
    ]
