from django.contrib.auth.models import AbstractUser
from django.db import models


LENGTH_LIMITS_CHAR_FIELDS = 150


class User(AbstractUser):
    """Модель пользователя."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
    ]
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

    class Meta:
        ordering = ('phone_number',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    name = models.CharField(
        'Название', max_lemax_length=LENGTH_LIMITS_CHAR_FIELDS)
    description = models.TextField('Описание')
    monthly_price = models.FloatField(
        'Цена подписки за месяц', decimal_places=2)
    semi_annual_price = models.FloatField(
        'Цена подписки за полгода', decimal_places=2)
    annual_price = models.FloatField('Цена подписки за год', decimal_places=2)
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
