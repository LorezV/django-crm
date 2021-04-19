from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from django.utils import timezone
from app.bot.jobs_utils import offer_master_order

# Create your models here.
class User(AbstractUser):
    pass


class City(models.Model):
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        
    title = models.CharField(max_length=128, verbose_name='Город', null=True, blank=True)

    def __str__(self):
        return self.title

class TelegramProfile(models.Model):
    class Meta:
        verbose_name = "Телеграм профиль"
        verbose_name_plural = "Телеграм профиля"

    telegram_first_name = models.CharField(
        max_length=128, verbose_name='Имя')
    telegram_last_name = models.CharField(
        max_length=128, verbose_name='Фамилия', blank=True, null=True)
    telegram_username = models.CharField(
        max_length=128, verbose_name='Telegram имя пользователя', blank=True, null=True)
    telegram_chat_id = models.CharField(max_length=128, verbose_name='Telegram id чата', unique=True)
    is_master = models.BooleanField(verbose_name='Является мастером?', blank=True, default=False)
    is_operator = models.BooleanField(verbose_name='Является оператором?', blank=True, default=False)
    percents = models.CharField(max_length=512, verbose_name='Проценты', help_text='[от-до%процент, от-до%процент...]. Если интервалы пересекаются, будет выбран первый в списке.', blank=False, default='0-2999%35,3000-999999%50') #amountFrom-amountTo%percent,amountFrom-amountTo%percent,amountFrom-amountTo%percent

    def __str__(self):
        string = self.telegram_first_name + ' ' + self.telegram_last_name
        if self.telegram_username:
            string += ' (@' + self.telegram_username + ')'
        return string
    
    def save(self, *args, **kwargs):
        self.percents = self.percents.replace(' ', '')
        super().save(*args, **kwargs)

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

    create_date = models.DateTimeField(verbose_name='Дата и время создания заказа.', auto_now_add=True)
    working_date = models.DateTimeField(verbose_name='Когда начинать работу', blank=True, default=timezone.now()+timezone.timedelta(hours=1))
    closing_date = models.DateTimeField(verbose_name='Дата и время закрытия заказа.', null=True, blank=True)
    client_name = models.CharField(max_length=256, verbose_name='Имя клиента', blank=True, default='')
    master_advert_name = models.CharField(max_length=128,verbose_name='Рекламное имя ВМ', blank=True, null=True)
    client_adress = models.CharField(max_length=256, verbose_name='Адрес', blank=True, default='')
    client_phone = models.CharField(max_length=128, verbose_name='Телефон клиента', blank=True, default='')
    client_city = models.ForeignKey(
        to=City,
        related_name='client_city',
        related_query_name='client_cities',
        verbose_name='Город',
        null=True,
        on_delete=models.SET_NULL
    )
    order_type = models.CharField(max_length=1, verbose_name='Тип', choices=TypeChoice, default='N')
    order_status = models.CharField(max_length=1, verbose_name='Статус', choices=StatusChoice, default='W')
    comment = models.TextField(verbose_name='Проблема', blank=True, default='')
    announced_amounts = models.TextField(verbose_name='Цены озвучены', blank=True, default='')
    master = models.ForeignKey(
        TelegramProfile,
        on_delete=models.SET_NULL,
        related_name='orders',
        related_query_name='order',
        limit_choices_to={'is_master': True},
        verbose_name='ВМ',
        blank=True,
        null=True
    )
    master_requests = models.ManyToManyField(
        TelegramProfile,
        related_name='orders_request',
        related_query_name='order_request',
        limit_choices_to={'is_master': True},
        blank=True,
        verbose_name='Предложения ВМ',
    )
    amount = models.PositiveIntegerField(verbose_name='Цена услуг', default=0)
    master_comment = models.TextField(verbose_name='Комментарий мастера', blank=True, default='')
    cashed = models.BooleanField(verbose_name='Деньги собраны?', default=False, blank=True)
    cached_master_percent = models.PositiveIntegerField(verbose_name='Процент мастера.', default=0, blank=True)

    def get_absolute_url(self):
        return reverse_lazy('orders/detail', kwargs={'pk': self.id})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.master:
            for master in self.master_requests.all():
                print('boty')
                offer_master_order(master, self)
    
    @property
    def get_amount(self):
        if self.order_status == 'R':
            return self.amount
        return 0

    @property
    def get_master_amount(self):
        return int(self.get_amount * self.master_coef)

    @property
    def get_clear_amount(self):
        return int(self.get_amount - self.get_master_amount)
    
    @property
    def get_cashed_value(self):
        if self.cashed:
            return self.get_clear_amount
        return 0

    @property
    def master_coef(self):
        if self.master:
            for row in self.master.percents.split(','):
                values, percent = row.split('%')
                val1, val2 = values.split('-')
                if self.get_amount > int(val1) and self.get_amount < int(val2):
                    self.cached_master_percent = int(percent) / 100
                    self.save()
                    return self.cached_master_percent
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
