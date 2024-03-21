from django.contrib.auth.models import AbstractUser
from django.db import models


LENGTH_LIMITS_CHAR_FIELDS = 150


class User(AbstractUser):
    """Модель пользователя."""

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    phone_number = models.IntegerField(
        'Номер телефона',
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        'Имя',
        max_length=LENGTH_LIMITS_CHAR_FIELDS,
    )
    middle_name = models.CharField(
        'Отчество',
        max_length=LENGTH_LIMITS_CHAR_FIELDS,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=LENGTH_LIMITS_CHAR_FIELDS,
    )
    account_balance = models.DecimalField(
        'Счет', max_digits=10, decimal_places=2)
    cashback = models.DecimalField('Кэшбек', max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('phone_number',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    """Модель подписок"""
    name = models.CharField(
        'Название', max_length=LENGTH_LIMITS_CHAR_FIELDS)
    description = models.TextField('Описание')
    monthly_price = models.DecimalField(
        'Цена подписки за месяц', max_digits=5, decimal_places=2)
    semi_annual_price = models.DecimalField(
        'Цена подписки за полгода', max_digits=5, decimal_places=2)
    annual_price = models.DecimalField(
        'Цена подписки за год', max_digits=5, decimal_places=2)
    users = models.ManyToManyField(
        User,
        through='UserSubscription',
        verbose_name='Пользователи'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class UserSubscription(models.Model):
    """Модель связи M2M"""
    user = models.ForeignKey(
        User,
        related_name='usersubscriptions',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='usersubscriptions',
        verbose_name='Подписка'
    )
    start_date = models.DateField(
        'Дата начала подписки', auto_now=True, auto_now_add=False)
    end_date = models.DateField('Дата окончания подписки', blank=True)

    class Meta:
        ordering = ('user',)
        verbose_name = 'Пользователь/Подписка'
        verbose_name_plural = 'Пользователи/Подписки'
        constraints = [models.UniqueConstraint(
            fields=['user', 'subscription'],
            name='unique_user_subscription'
        )]
