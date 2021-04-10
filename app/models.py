from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    pass


class TelegramProfile(models.Model):
    class Meta:
        verbose_name = "Телеграм профиль"
        verbose_name_plural = "Телеграм профиля"

    telegram_first_name = models.CharField(
        max_length=128, verbose_name='Имя', blank=True)
    telegram_last_name = models.CharField(
        max_length=128, verbose_name='Фамилия', blank=True)
    telegram_username = models.CharField(
        max_length=128, verbose_name='Telegram имя пользователя', blank=True, null=True)
    telegram_chat_id = models.CharField(max_length=128, verbose_name='Telegram id чата')
    is_master = models.BooleanField(verbose_name='Является мастером?', blank=True, default=False)
    is_operator = models.BooleanField(verbose_name='Является оператором?', blank=True, default=False)

    def __str__(self):
        string = self.telegram_first_name + ' ' + self.telegram_last_name
        if self.telegram_username:
            string += ' (' + self.telegram_username + ')'
        return string

    def get_absolute_url(self):
        return reverse_lazy('masters/detail', kwargs={'pk': self.id})


class Order(models.Model):
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    TypeChoice = (
        ('G', 'Гарантия'),
        ('N', 'Обычный'),
    )
    StatusChoice = (
        ('R', 'Готово'),
        ('W', 'Ждет'),
        ('C', 'Отменен'),
        ('J', 'В работе'),
        ('M', 'Модернизация')
    )

    create_date = models.DateTimeField(
        verbose_name='Дата и время создания заказа.', auto_now_add=True)
    working_date = models.DateTimeField(verbose_name='Когда начинать работу', default=timezone.now()+timezone.timedelta(hours=1))
    closing_date = models.DateTimeField(
        verbose_name='Дата и время закрытия заказа.', null=True, blank=True)
    client_name = models.CharField(
        max_length=256, verbose_name='Имя клиента', blank=True)
    client_adress = models.CharField(
        max_length=256, verbose_name='Адрес', blank=True)
    client_phone = models.CharField(
        max_length=128, verbose_name='Телефон клиента', blank=True)
    client_city = models.CharField(
        max_length=128, verbose_name='Город')
    order_type = models.CharField(
        max_length=1, verbose_name='Тип', choices=TypeChoice, default='N')
    order_status = models.CharField(
        max_length=1, verbose_name='Статус', choices=StatusChoice, default='W')
    comment = models.TextField(
        verbose_name='Коментарий', blank=True, default='')
    master = models.ForeignKey(
        TelegramProfile,
        on_delete=models.SET_NULL,
        related_name='orders',
        related_query_name='order',
        limit_choices_to={'is_master': True},
        blank=True,
        null=True
    )
    master_requests = models.ManyToManyField(
        TelegramProfile,
        related_name='orders_request',
        related_query_name='order_request',
        limit_choices_to={'is_master': True},
        blank=True,
        verbose_name='Предложения мастерам'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Цена услуг', default=0)
    master_comment = models.TextField(
        verbose_name='Комментарий мастера', blank=True, default='')

    def get_absolute_url(self):
        return reverse_lazy('orders/detail', kwargs={'pk': self.id})

    @property
    def master_coef(self):
        if self.amount <= 3000:
            _coef = 0.35
        elif self.amount > 3000:
            _coef = 0.5
        else:
            return Null
        return _coef

    @property
    def master_amount(self):
        if self.amount:
            return int(self.amount * self.master_coef)
        return 0

    @property
    def clear_amount(self):
        if self.amount:
            return int(self.amount - (self.amount * self.master_coef))
        return 0

    @property
    def type_verbose(self):
        if (self.order_type):
            return dict(Order.TypeChoice)[self.order_type]
        return ''

    @property
    def status_verbose(self):
        if (self.order_status):
            return dict(Order.StatusChoice)[self.order_status]
        return ''
